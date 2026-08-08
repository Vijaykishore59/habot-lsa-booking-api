from flask import Blueprint, request

from app.models.lsa_profile import LSAProfile


lsas_bp = Blueprint(
    "lsas",
    __name__,
    url_prefix="/api/v1/lsas"
)


@lsas_bp.get("/search/")
def search_lsas():
    """
    Search available Learning Support Assistants
    ---
    tags:
      - LSA
    parameters:
      - name: skill
        in: query
        type: string
        required: false
        description: Skill to search for
        example: Autism
    responses:
      200:
        description: Successfully retrieved available LSAs
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            count:
              type: integer
              example: 1
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: Ananya Sharma
                  email:
                    type: string
                    example: ananya@example.com
                  skills:
                    type: string
                    example: Autism, ADHD, Dyslexia
                  hourly_rate:
                    type: number
                    example: 25.0
                  is_active:
                    type: boolean
                    example: true
    """

    skill = request.args.get("skill", "").strip()

    query = LSAProfile.query.filter(
        LSAProfile.is_active.is_(True)
    )

    if skill:
        query = query.filter(
            LSAProfile.skills.ilike(f"%{skill}%")
        )

    lsas = query.order_by(
        LSAProfile.id.asc()
    ).all()

    return {
        "status": "success",
        "count": len(lsas),
        "data": [
            {
                "id": lsa.id,
                "name": lsa.name,
                "email": lsa.email,
                "skills": lsa.skills,
                "hourly_rate": float(lsa.hourly_rate),
                "is_active": lsa.is_active
            }
            for lsa in lsas
        ]
    }, 200