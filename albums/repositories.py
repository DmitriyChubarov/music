from django.db.models import QuerySet

class BaseRepository:
    def get_objects(model) -> QuerySet:
        return model.objects.all()

