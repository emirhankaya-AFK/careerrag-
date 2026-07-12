from typing import List, Dict, Any

class MatchingAgent:
    def calculate_match_score(self, cv_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes CV to Job match score based on:
        - Required Skills Match (60%)
        - Experience Level Fit (20%)
        - Location Fit (20%)
        """
        cv_skills = [sk.lower() for sk in cv_data.get("skills", [])]
        job_req_skills = [sk.lower() for sk in job_data.get("required_skills", [])]
        
        # 1. Required Skills Match (60%)
        if not job_req_skills:
            skills_score = 1.0
        else:
            matched_skills = [sk for sk in job_req_skills if sk in cv_skills]
            skills_score = len(matched_skills) / len(job_req_skills)
            
        # 2. Experience Level Fit (20%)
        job_level = job_data.get("experience_level", "Mid").lower()
        
        # Determine candidate level based on experience summary
        exp_list = cv_data.get("experience", [])
        total_months = 0
        for exp in exp_list:
            duration_str = exp.get("duration", "").lower()
            # Simple heuristic parser for durations
            import re
            years_match = re.search(r'(\d+)\s*year', duration_str)
            months_match = re.search(r'(\d+)\s*month', duration_str)
            if years_match:
                total_months += int(years_match.group(1)) * 12
            if months_match:
                total_months += int(months_match.group(1))
                
        candidate_years = total_months / 12
        candidate_level = "junior" if candidate_years < 2 else "mid" if candidate_years < 6 else "senior"
        
        # Scoring grid
        level_score = 0.5
        if job_level == candidate_level:
            level_score = 1.0
        elif job_level == "junior" and candidate_level in ["mid", "senior"]:
            level_score = 1.0  # Overqualified fits junior roles
        elif job_level == "mid" and candidate_level == "senior":
            level_score = 0.9
        elif job_level == "mid" and candidate_level == "junior":
            level_score = 0.6
        elif job_level == "senior" and candidate_level == "mid":
            level_score = 0.7
        elif job_level == "senior" and candidate_level == "junior":
            level_score = 0.3
            
        # 3. Location Fit (20%)
        job_loc = job_data.get("location", "").lower()
        if "remote" in job_loc:
            location_score = 1.0
        else:
            # We assume a moderate location fit by default
            location_score = 0.8
            
        # Calculate final weighted score
        final_score = (skills_score * 0.6) + (level_score * 0.2) + (location_score * 0.2)
        final_score_pct = int(final_score * 100)
        
        return {
            "match_score": min(100, max(0, final_score_pct)),
            "skills_score": int(skills_score * 100),
            "level_score": int(level_score * 100),
            "location_score": int(location_score * 100),
            "candidate_years": round(candidate_years, 1),
            "candidate_level": candidate_level.capitalize()
        }

matching_agent = MatchingAgent()
