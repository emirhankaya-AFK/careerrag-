import chromadb
from typing import List, Dict, Any, Optional
from ..config.settings import settings
from .llm_service import llm_service

class CareerRAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        self.collection_name = "jobs"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_job(self, job_id: int, title: str, description: str, company: str, skills: List[str]):
        """
        Embeds a job listing description and indexes it.
        """
        embedding = llm_service.generate_embeddings(description)
        
        self.collection.add(
            ids=[f"job_{job_id}"],
            embeddings=[embedding],
            metadatas=[{
                "job_id": job_id,
                "title": title,
                "company": company,
                "skills": ",".join(skills)
            }],
            documents=[description]
        )

    def match_jobs(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches indexed jobs semantic matching.
        """
        query_embedding = llm_service.generate_embeddings(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        formatted_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)
            ids = results["ids"][0]

            for i in range(len(docs)):
                formatted_results.append({
                    "id": ids[i],
                    "content": docs[i],
                    "metadata": metas[i],
                    "distance": distances[i]
                })

        return formatted_results

rag_service = CareerRAGService()
