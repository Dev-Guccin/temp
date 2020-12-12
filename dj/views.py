from rest_framework import viewsets
from .models import Essay
from .serializer import EssaySerializer
from rest_framework.filters import SearchFilter
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pickle


class PostViewSet(viewsets.ModelViewSet):

    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    filter_backends = [SearchFilter]
    search_fields = ('title','body')

    def perform_create(self, serializer):
        serializer.save(author= self.request.user)


    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            qs= qs.filter(author = self.request.user)
        else:
            qs = qs.none()



        return qs

@csrf_exempt
def run(request):
    # 값을 받아서 처리해보자
    if request.method == 'POST':
        print("post")
        json_data = json.loads(request.body)
        size_list = [json_data['length'],json_data['waist'],json_data['thigh'],json_data['rise'],json_data['hem']]
        print(size_list)
        kmeans = pickle.load(open("save.pkl", "rb")) # 모델 로드
        tmp = kmeans.predict([size_list])
    return HttpResponse(tmp)