"""DSPy modules and signatures for the application."""

import dspy
from typing import Optional


class BasicQA(dspy.Signature):
    """Answer questions with short factual answers."""
    
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")


class ChainOfThought(dspy.Module):
    """Chain of Thought reasoning module."""
    
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(BasicQA)
    
    def forward(self, question: str):
        """Process question with chain of thought."""
        return self.generate_answer(question=question)


class RAG(dspy.Module):
    """Retrieval-Augmented Generation module."""
    
    def __init__(self, num_passages: int = 3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(BasicQA)
    
    def forward(self, question: str):
        """Process question with RAG."""
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)


def configure_lm(model: str = "gpt-4o-mini", api_key: Optional[str] = None):
    """Configure DSPy language model."""
    if api_key:
        lm = dspy.LM(model=model, api_key=api_key)
    else:
        lm = dspy.LM(model=model)
    dspy.configure(lm=lm)
    return lm
