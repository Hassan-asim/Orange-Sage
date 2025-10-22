"""
Sandbox Service for Orange Sage
Handles Docker container management for agent execution
"""

import asyncio
import logging
import docker
from datetime import datetime
from typing import Dict, List, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class SandboxService:
    """Service for managing Docker sandboxes"""
    
    def __init__(self):
        self.docker_client = None
        self.active_sandboxes: Dict[str, Dict[str, Any]] = {}
        self._initialize_docker()
    
    def _initialize_docker(self):
        """Initialize Docker client"""
        try:
            self.docker_client = docker.from_env()
            # Test connection
            self.docker_client.ping()
            logger.info("✅ Docker client initialized successfully")
        except Exception as e:
            logger.info("ℹ️  Docker not available - using mock sandbox mode (this is OK for local development)")
            logger.debug(f"Docker error details: {e}")
            self.docker_client = None
    
    async def create_sandbox(self, agent_id: str) -> Dict[str, Any]:
        """Create a new sandbox for agent execution"""
        if not self.docker_client:
            logger.warning("Docker not available - using mock sandbox for local development")
            return {
                "sandbox_id": f"mock_sandbox_{agent_id}",
                "status": "running",
                "container_id": None,
                "created_at": datetime.utcnow()
            }
        
        try:
            # Create Docker container
            container = self.docker_client.containers.run(
                image=settings.SANDBOX_IMAGE,
                name=f"orange_sage_sandbox_{agent_id}",
                detach=True,
                network=settings.DOCKER_NETWORK,
                mem_limit=settings.SANDBOX_MEMORY_LIMIT,
                cpu_quota=int(float(settings.SANDBOX_CPU_LIMIT) * 100000),
                environment={
                    "AGENT_ID": agent_id,
                    "SANDBOX_MODE": "true"
                },
                volumes={
                    "/tmp/orange_sage_uploads": {"bind": "/workspace", "mode": "rw"}
                },
                working_dir="/workspace",
                remove=False
            )
            
            # Wait for container to be ready
            await asyncio.sleep(2)
            
            # Get container info
            container.reload()
            
            sandbox_info = {
                "workspace_id": container.id,
                "container_id": container.id,
                "container_name": container.name,
                "api_url": f"http://{container.name}:8000",
                "auth_token": f"token_{agent_id}",
                "agent_id": agent_id,
                "status": "running"
            }
            
            # Store sandbox info
            self.active_sandboxes[agent_id] = sandbox_info
            
            logger.info(f"Created sandbox for agent {agent_id}: {container.id}")
            
            return sandbox_info
            
        except Exception as e:
            logger.error(f"Error creating sandbox for agent {agent_id}: {e}")
            raise
    
    async def destroy_sandbox(self, agent_id: str) -> bool:
        """Destroy a sandbox"""
        try:
            if agent_id not in self.active_sandboxes:
                logger.warning(f"Sandbox for agent {agent_id} not found")
                return False
            
            sandbox_info = self.active_sandboxes[agent_id]
            container_id = sandbox_info["container_id"]
            
            # Get container
            try:
                container = self.docker_client.containers.get(container_id)
                
                # Stop and remove container
                container.stop(timeout=10)
                container.remove(force=True)
                
                logger.info(f"Destroyed sandbox for agent {agent_id}: {container_id}")
                
            except docker.errors.NotFound:
                logger.warning(f"Container {container_id} not found")
            except Exception as e:
                logger.error(f"Error destroying container {container_id}: {e}")
            
            # Remove from active sandboxes
            del self.active_sandboxes[agent_id]
            
            return True
            
        except Exception as e:
            logger.error(f"Error destroying sandbox for agent {agent_id}: {e}")
            return False
    
    async def get_sandbox_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get sandbox status"""
        if agent_id not in self.active_sandboxes:
            return None
        
        sandbox_info = self.active_sandboxes[agent_id]
        container_id = sandbox_info["container_id"]
        
        try:
            container = self.docker_client.containers.get(container_id)
            container.reload()
            
            return {
                "agent_id": agent_id,
                "container_id": container_id,
                "status": container.status,
                "created_at": container.attrs["Created"],
                "state": container.attrs["State"]
            }
            
        except docker.errors.NotFound:
            return None
        except Exception as e:
            logger.error(f"Error getting sandbox status for agent {agent_id}: {e}")
            return None
    
    async def execute_command(self, agent_id: str, command: str) -> Dict[str, Any]:
        """Execute command in sandbox"""
        try:
            if agent_id not in self.active_sandboxes:
                raise ValueError(f"Sandbox for agent {agent_id} not found")
            
            sandbox_info = self.active_sandboxes[agent_id]
            container_id = sandbox_info["container_id"]
            
            container = self.docker_client.containers.get(container_id)
            
            # Execute command
            result = container.exec_run(
                command,
                workdir="/workspace",
                environment={"AGENT_ID": agent_id}
            )
            
            return {
                "exit_code": result.exit_code,
                "stdout": result.output.decode("utf-8") if result.output else "",
                "stderr": "",
                "success": result.exit_code == 0
            }
            
        except Exception as e:
            logger.error(f"Error executing command in sandbox {agent_id}: {e}")
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False
            }
    
    async def upload_file(self, agent_id: str, file_path: str, content: bytes) -> bool:
        """Upload file to sandbox"""
        try:
            if agent_id not in self.active_sandboxes:
                raise ValueError(f"Sandbox for agent {agent_id} not found")
            
            sandbox_info = self.active_sandboxes[agent_id]
            container_id = sandbox_info["container_id"]
            
            container = self.docker_client.containers.get(container_id)
            
            # Create file in container
            import io
            file_obj = io.BytesIO(content)
            
            # Use put_archive to upload file
            container.put_archive("/workspace", file_obj.getvalue())
            
            logger.info(f"Uploaded file {file_path} to sandbox {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading file to sandbox {agent_id}: {e}")
            return False
    
    async def download_file(self, agent_id: str, file_path: str) -> Optional[bytes]:
        """Download file from sandbox"""
        try:
            if agent_id not in self.active_sandboxes:
                raise ValueError(f"Sandbox for agent {agent_id} not found")
            
            sandbox_info = self.active_sandboxes[agent_id]
            container_id = sandbox_info["container_id"]
            
            container = self.docker_client.containers.get(container_id)
            
            # Get file from container
            stream, stat = container.get_archive(f"/workspace/{file_path}")
            
            # Read the stream
            import tarfile
            import io
            
            file_obj = io.BytesIO()
            for chunk in stream:
                file_obj.write(chunk)
            
            file_obj.seek(0)
            
            # Extract file from tar
            with tarfile.open(fileobj=file_obj, mode='r') as tar:
                for member in tar.getmembers():
                    if member.name.endswith(file_path):
                        return tar.extractfile(member).read()
            
            return None
            
        except Exception as e:
            logger.error(f"Error downloading file from sandbox {agent_id}: {e}")
            return None
    
    async def cleanup_all(self):
        """Cleanup all active sandboxes"""
        try:
            for agent_id in list(self.active_sandboxes.keys()):
                await self.destroy_sandbox(agent_id)
            
            logger.info("Cleaned up all sandboxes")
            
        except Exception as e:
            logger.error(f"Error during sandbox cleanup: {e}")
    
    def get_active_sandboxes(self) -> List[Dict[str, Any]]:
        """Get list of active sandboxes"""
        return list(self.active_sandboxes.values())
