import streamlit as st
from trulens_eval import (
    Tru,
    Feedback,
    TruLlama,
    OpenAI as TruLensOpenAI
)
from trulens_eval.feedback import Groundedness
import numpy as np
from dotenv import load_dotenv
load_dotenv()

truelens_openai = TruLensOpenAI()
tru = Tru()

def get_tru():
    return tru

# underscores in func params are to avoid hashing argument
@st.cache_resource
def load_trulens(_query_engine, app_id):
    print("loading trulens")
    
    # DB may reset on browser refresh, so feel free to comment this out.
    tru.reset_database()

    qa_relevance = (
        Feedback(truelens_openai.relevance_with_cot_reasons, name="Answer Relevance")
        .on_input_output()
    )

    qs_relevance = (
        Feedback(truelens_openai.relevance_with_cot_reasons, name = "Context Relevance")
        .on_input()
        .on(TruLlama.select_source_nodes().node.text)
        .aggregate(np.mean)
    )

    #grounded = Groundedness(groundedness_provider=openai, summarize_provider=openai)
    grounded = Groundedness(groundedness_provider=truelens_openai)

    groundedness = (
        Feedback(grounded.groundedness_measure_with_cot_reasons, name="Groundedness")
            .on(TruLlama.select_source_nodes().node.text)
            .on_output()
            .aggregate(grounded.grounded_statements_aggregator)
    )

    feedbacks = [qa_relevance, qs_relevance, groundedness]
    tru_recorder = TruLlama(
        _query_engine,
        app_id=app_id,
        feedbacks=feedbacks
        )

    return tru_recorder