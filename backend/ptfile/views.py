import torch
import torch.nn as nn
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image
import torchvision.transforms as transforms
from .ptfileserializers import ImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class LabelView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):

        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_file = serializer.validated_data['image']



        # 이미지 전처리
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        image_tensor = transform(image_file)

        # 모델 로드 및 추론
        model = torch.load('ptfile/best.pt')
        model.load_state_dict(torch.load('ptfile/best.pt'))
        model.eval()
        with torch.no_grad():
            output = model(image_tensor.unsqueeze(0))

        # 라벨링 결과 추출
        predicted_label = output.argmax().item()

        return Response({'label': predicted_label})
