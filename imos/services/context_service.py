from imos.services.query_service import QueryService

class ContextService:
    def executive_summary(self):
        summary = QueryService().summary()
        return {
            'system': 'IMOS',
            'status': 'active-build',
            'inventory': summary,
            'thesis': 'Institutional memory as executable organizational cognition'
        }

