import sys
import os
from services.rag_service import process_document,do_query

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def test_pipeline():
    file_path = "test_text.pdf"
    process_document(file_path)
    response = do_query("Impatto ambientale  dell'impianto")
    print("\n ANSWER: ")
    print(response)

if __name__ == "__main__":
    test_pipeline()