from nlp_engine.processor import NLPProcessor
from rag_system.retriever import RAGSystem
from database.db_handler import DatabaseHandler
from ml_pipeline.analyzer import MLPipeline
from visualization.dashboard import Dashboard
import os
from dotenv import load_dotenv
import tensorflow as tf

def limit_memory():
    """Limit TensorFlow memory growth"""
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    
    # Limit CPU memory usage
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.config.threading.set_intra_op_parallelism_threads(1)

def main():
    # Setup memory limits
    limit_memory()
    
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    nlp_processor = NLPProcessor()
    rag_system = RAGSystem("knowledge_base/")
    db_handler = DatabaseHandler()
    ml_pipeline = MLPipeline()
    dashboard = Dashboard()
    
    # Start the dashboard
    dashboard.run_server(debug=True)

if __name__ == "__main__":
    main() 