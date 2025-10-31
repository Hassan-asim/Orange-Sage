"use client"

import type React from "react"
import { useState } from "react"
import { ChevronDown } from "lucide-react"

const faqData = [
   {
        "question": "What is Orange Sage and who is it for?",
        "answer": "Orange Sage is an AI-powered penetration testing platform designed for security teams, developers, and organizations who want to find and fix vulnerabilities before they reach production. It's perfect for teams seeking automated security testing that matches the quality of elite penetration testers."
      },
      {
        "question": "How does Orange Sage's AI penetration testing work?",
        "answer": "Our AI agents run real attacks against your applications, just like human penetration testers. They scan APIs, web apps, networks, GitHub/GitLab code, and CI/CD pipelines, then provide validated findings with proof-of-concept exploits and detailed reports."
      },
      {
        "question": "What makes Orange Sage different from traditional security scanners?",
        "answer": "Unlike traditional scanners that produce false positives, Orange Sage validates every finding with actual exploits. It launches real-world attacks to confirm vulnerabilities exist, provides proof-of-concept scripts, and generates production-ready fixes automatically."
      },
      {
        "question": "How fast is Orange Sage compared to manual penetration testing?",
        "answer": "Orange Sage is 30× faster than manual pentesting. What takes weeks with traditional methods can be completed in hours. Plus, it runs continuously 24/7, providing round-the-clock security monitoring."
      },
      {
        "question": "What types of applications can Orange Sage test?",
        "answer": "Orange Sage provides complete coverage across APIs, web applications, networks, GitHub and GitLab repositories, and CI/CD pipelines. It can test any application or infrastructure component that needs security validation."
      },
      {
        "question": "Is my code and data secure with Orange Sage?",
        "answer": "Absolutely. We use enterprise-grade security measures including end-to-end encryption and compliance with industry standards. For enterprise customers, we offer VPC and on-premises deployment options to ensure your sensitive data never leaves your environment."
      }
]

interface FAQItemProps {
  question: string
  answer: string
  isOpen: boolean
  onToggle: () => void
}

const FAQItem = ({ question, answer, isOpen, onToggle }: FAQItemProps) => {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault()
    onToggle()
  }
  return (
    <div
      className={`w-full bg-[rgba(231,236,235,0.08)] shadow-[0px_2px_4px_rgba(0,0,0,0.16)] overflow-hidden rounded-[10px] outline outline-1 outline-border outline-offset-[-1px] transition-all duration-500 ease-out cursor-pointer`}
      onClick={handleClick}
    >
      <div className="w-full px-5 py-[18px] pr-4 flex justify-between items-center gap-5 text-left transition-all duration-300 ease-out">
        <div className="flex-1 text-foreground text-base font-medium leading-6 break-words">{question}</div>
        <div className="flex justify-center items-center">
          <ChevronDown
            className={`w-6 h-6 text-muted-foreground-dark transition-all duration-500 ease-out ${isOpen ? "rotate-180 scale-110" : "rotate-0 scale-100"}`}
          />
        </div>
      </div>
      <div
        className={`overflow-hidden transition-all duration-500 ease-out ${isOpen ? "max-h-[500px] opacity-100" : "max-h-0 opacity-0"}`}
        style={{
          transitionProperty: "max-height, opacity, padding",
          transitionTimingFunction: "cubic-bezier(0.4, 0, 0.2, 1)",
        }}
      >
        <div
          className={`px-5 transition-all duration-500 ease-out ${isOpen ? "pb-[18px] pt-2 translate-y-0" : "pb-0 pt-0 -translate-y-2"}`}
        >
          <div className="text-foreground/80 text-sm font-normal leading-6 break-words">{answer}</div>
        </div>
      </div>
    </div>
  )
}

export function FAQSection() {
  const [openItems, setOpenItems] = useState<Set<number>>(new Set())
  const toggleItem = (index: number) => {
    const newOpenItems = new Set(openItems)
    if (newOpenItems.has(index)) {
      newOpenItems.delete(index)
    } else {
      newOpenItems.add(index)
    }
    setOpenItems(newOpenItems)
  }
  return (
    <section className="w-full pt-[66px] pb-20 md:pb-40 px-5 relative flex flex-col justify-center items-center">
      <div className="w-[300px] h-[500px] absolute top-[150px] left-1/2 -translate-x-1/2 origin-top-left rotate-[-33.39deg] bg-primary/10 blur-[100px] z-0" />
      <div className="self-stretch pt-8 pb-8 md:pt-14 md:pb-14 flex flex-col justify-center items-center gap-2 relative z-10">
        <div className="flex flex-col justify-start items-center gap-4">
          <h2 className="w-full max-w-[435px] text-center text-foreground text-4xl font-semibold leading-10 break-words">
            Frequently Asked Questions
          </h2>
          <p className="self-stretch text-center text-muted-foreground text-sm font-medium leading-[18.20px] break-words">
            Everything you need to know about Pointer and how it can transform your development workflow
          </p>
        </div>
      </div>
      <div className="w-full max-w-[600px] pt-0.5 pb-10 flex flex-col justify-start items-start gap-4 relative z-10">
        {faqData.map((faq, index) => (
          <FAQItem key={index} {...faq} isOpen={openItems.has(index)} onToggle={() => toggleItem(index)} />
        ))}
      </div>
    </section>
  )
}
