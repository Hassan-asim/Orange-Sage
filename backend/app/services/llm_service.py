"""
LLM Service for Orange Sage
Handles LLM API calls and model management
"""

import logging
import openai
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for managing LLM interactions"""
    
    def __init__(self):
        self.openai_client = None
        self.gemini_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize LLM clients"""
        try:
            # Initialize OpenAI
            if settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
                self.openai_client = openai
                logger.info("OpenAI client initialized")
            
            # Initialize Gemini
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_client = genai
                logger.info("Gemini client initialized")
                
        except Exception as e:
            logger.error(f"Error initializing LLM clients: {e}")
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """Generate response using LLM"""
        try:
            # Use default model if not specified
            if not model:
                model = settings.DEFAULT_LLM_MODEL
            
            # Try OpenAI first
            if self.openai_client and "gpt" in model.lower():
                return await self._generate_openai_response(
                    messages, model, temperature, max_tokens
                )
            
            # Try Gemini as fallback
            elif self.gemini_client and "gemini" in model.lower():
                return await self._generate_gemini_response(
                    messages, model, temperature, max_tokens
                )
            
            # Fallback to available model
            if self.openai_client:
                return await self._generate_openai_response(
                    messages, settings.DEFAULT_LLM_MODEL, temperature, max_tokens
                )
            elif self.gemini_client:
                return await self._generate_gemini_response(
                    messages, settings.FALLBACK_LLM_MODEL, temperature, max_tokens
                )
            
            raise Exception("No LLM client available")
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise
    
    async def _generate_openai_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        try:
            response = await self.openai_client.ChatCompletion.acreate(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": model,
                "usage": response.usage.dict() if response.usage else None,
                "provider": "openai"
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _generate_gemini_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Generate response using Gemini"""
        try:
            # Convert messages to Gemini format
            # Gemini expects a single prompt string or a list of content parts
            prompt_parts = []
            system_prompt = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                elif msg["role"] == "user":
                    prompt_parts.append(msg["content"])
                elif msg["role"] == "assistant":
                    # For conversation history, we'll include assistant responses
                    prompt_parts.append(f"Assistant: {msg['content']}")
            
            # Combine system prompt with user messages
            full_prompt = system_prompt
            if prompt_parts:
                full_prompt += "\n\n" + "\n\n".join(prompt_parts)
            
            # Generate response
            model_instance = self.gemini_client.GenerativeModel(model)
            response = await model_instance.generate_content_async(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            
            # Check for blocked content or other issues
            if not response.candidates:
                raise Exception("No candidates returned from Gemini API")
            
            candidate = response.candidates[0]
            if candidate.finish_reason == 2:  # SAFETY
                raise Exception("Content was blocked by Gemini safety filters")
            elif candidate.finish_reason == 3:  # RECITATION
                raise Exception("Content was blocked due to recitation concerns")
            elif candidate.finish_reason == 4:  # OTHER
                raise Exception("Content generation failed for other reasons")
            
            # Check if response has content
            if not candidate.content or not candidate.content.parts:
                raise Exception("No content parts in Gemini response")
            
            # Extract text content
            content = ""
            for part in candidate.content.parts:
                if hasattr(part, 'text') and part.text:
                    content += part.text
            
            if not content:
                raise Exception("No text content found in Gemini response")
            
            return {
                "content": content,
                "model": model,
                "usage": None,  # Gemini doesn't provide usage info in the same format
                "provider": "gemini"
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        models = []
        
        if self.openai_client:
            models.extend([
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
                "gpt-3.5-turbo"
            ])
        
        if self.gemini_client:
            try:
                # Try to get available models from Gemini API
                available_models = self.gemini_client.list_models()
                for model in available_models:
                    if 'generateContent' in model.supported_generation_methods:
                        models.append(model.name.replace('models/', ''))
            except Exception as e:
                logger.warning(f"Could not fetch Gemini models dynamically: {e}")
                # Fallback to known models
                models.extend([
                    "gemini-1.5-pro",
                    "gemini-1.5-flash-002",
                    "gemini-2.0-flash-lite",
                    "gemini-2.0-flash-exp"
                ])
        
        return models
    
    def is_model_available(self, model: str) -> bool:
        """Check if a model is available"""
        return model in self.get_available_models()
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test LLM connections"""
        results = {
            "openai": {"available": False, "error": None},
            "gemini": {"available": False, "error": None}
        }
        
        # Test OpenAI
        if self.openai_client:
            try:
                await self._generate_openai_response(
                    [{"role": "user", "content": "Hello"}],
                    "gpt-3.5-turbo",
                    0.1,
                    10
                )
                results["openai"]["available"] = True
            except Exception as e:
                results["openai"]["error"] = str(e)
        
        # Test Gemini
        if self.gemini_client:
            try:
                # Try multiple model names in order of preference
                gemini_models = ["gemini-2.0-flash-lite", "gemini-1.5-flash-002", "gemini-1.5-pro"]
                success = False
                
                for model in gemini_models:
                    try:
                        await self._generate_gemini_response(
                            [{"role": "user", "content": "Hello"}],
                            model,
                            0.1,
                            10
                        )
                        results["gemini"]["available"] = True
                        success = True
                        break
                    except Exception as model_error:
                        logger.warning(f"Model {model} failed: {model_error}")
                        continue
                
                if not success:
                    results["gemini"]["error"] = "All Gemini models failed to respond"
                    
            except Exception as e:
                results["gemini"]["error"] = str(e)
        
        return results
