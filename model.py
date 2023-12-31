
# Importing required libraries
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(review):
    tokens = tokenizer.encode(review, return_tensors="pt")
    result = model(tokens).logits
    return int(torch.argmax(result))+1