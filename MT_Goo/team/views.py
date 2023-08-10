from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import teamSpaceSerializer,teamUserSerializer, teamLodgingScrapSerializer, teamRecreationScrapSerializer, createTeamShoppingSerializer, teamShoppingScrapSerializer, teamScrapListSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import teamUser, teamSpace, teamLodgingScrap, teamRecreationScrap, teamShoppingScrap
from rest_framework.response import Response
from rest_framework import status
from lodging.serializers import lodgingMainSerializer
from lodging.models import lodgingMain
from recreation.serializers import recreationMainSerializer
from recreation.models import recreationMain

class teamSpaceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'teamName': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['teamName']
    ), responses={status.HTTP_200_OK: teamSpaceSerializer})
    def post(self, request):
        serializer = teamSpaceSerializer(data = request.data)
        if serializer.is_valid():
            team = serializer.save()
            user = teamUser.objects.create(user = request.user, teamSpace = team)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @swagger_auto_schema(responses={status.HTTP_200_OK: teamSpaceSerializer})    
    def get(self, request):
        tUsers = teamUser.objects.filter(user=request.user)
        tSpaces = []
        for user in tUsers:
            tSpaces.append(user.teamSpace)
        serializer = teamSpaceSerializer(tSpaces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class joinTeamSpaceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'teamToken': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['teamToken']
    ), responses={status.HTTP_200_OK: teamUserSerializer})
    def post(self, request):
        try:
            teamToken = request.data['teamToken']
            team_space = teamSpace.objects.get(teamToken=teamToken)

            # 이미 가입한 경우 예외 처리
            if teamUser.objects.filter(user=request.user, teamSpace=team_space).exists():
                return Response({'error': 'Already joined this team space'}, status=status.HTTP_400_BAD_REQUEST)

            # 새로운 teamUser 객체 생성
            team_user = teamUser.objects.create(user=request.user, teamSpace=team_space)
            serializer = teamUserSerializer(team_user)  # 필요한 Serializer로 변경해야 함

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except teamSpace.DoesNotExist:
            return Response({'error': 'Team space not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class teamSpaceLodgingView(APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: lodgingMainSerializer})
    def get(self, request):
        teamToken = request.GET.get('teamToken')
        tSpace = teamSpace.objects.get(teamToken=teamToken)
        tLodgingScraps = teamLodgingScrap.objects.filter(teamSpace= tSpace)
        lodgings = []
        for tLodgingScrap in tLodgingScraps:
            lodgings.append(tLodgingScrap.lodging)
        serializer = lodgingMainSerializer(lodgings, many = True, context = {'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'teamToken': openapi.Schema(type=openapi.TYPE_STRING),
            'lodgingPk': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['teamToken', 'lodgingPk']
    ), responses={status.HTTP_200_OK: teamLodgingScrapSerializer})
    def post(self, request):
        try:
            teamToken = request.data['teamToken']
            lodgingPk = request.data['lodgingPk']
            tSpace = teamSpace.objects.get(teamToken=teamToken)
            lodging = lodgingMain.objects.get(pk=lodgingPk)

            # 이미 해당 lodging과 tSpace에 대한 teamLodgingScrap 객체가 존재하는지 확인
            existing_scrap = teamLodgingScrap.objects.filter(lodging=lodging, teamSpace=tSpace).first()
            if existing_scrap:
                existing_scrap.delete()  # 이미 존재할 경우 해당 객체 삭제
                return Response({"message": "Scrap deleted."}, status=status.HTTP_200_OK)
            else:
                tLodgingScrap = teamLodgingScrap.objects.create(lodging=lodging, teamSpace=tSpace)
                serializer = teamLodgingScrapSerializer(tLodgingScrap)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"error": "Required data not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        except teamSpace.DoesNotExist:
            return Response({"error": "TeamSpace not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except lodgingMain.DoesNotExist:
            return Response({"error": "Lodging not found."}, status=status.HTTP_404_NOT_FOUND)

class teamSpaceLodgingScrapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: teamScrapListSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='lodgingPk',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='헤더에 token 추가 및 params에 lodgingPk 추가',
            )
        ]
    )
    def get(self, request):
        try:
            lodgingPk = request.GET.get('lodgingPk')
            lodging = lodgingMain.objects.get(pk=lodgingPk)

            tUsers = teamUser.objects.filter(user=request.user)
            teamList = [tUser.teamSpace for tUser in tUsers]

            scrapedLodgings = teamLodgingScrap.objects.filter(lodging=lodging, teamSpace__in=teamList)
            scrapedTeam = [scrapedLodging.teamSpace for scrapedLodging in scrapedLodgings]

            serializer = teamScrapListSerializer(teamList, many=True, context={'scrapedTeam': scrapedTeam})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except lodgingMain.DoesNotExist:
            return Response({'error': 'Lodging not found'}, status=status.HTTP_404_NOT_FOUND)
        except teamUser.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class teamSpaceRecreationView(APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: recreationMainSerializer})
    def get(self, request):
        teamToken = request.GET.get('teamToken')
        tSpace = teamSpace.objects.get(teamToken=teamToken)
        tRecreationScraps = teamRecreationScrap.objects.filter(teamSpace= tSpace)
        recreations = []
        for tRecreationScrap in tRecreationScraps:
            recreations.append(tRecreationScrap.recreation)

        serializer = recreationMainSerializer(recreations, many = True, context = {'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'teamToken': openapi.Schema(type=openapi.TYPE_STRING),
            'recreationPk': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['teamToken', 'recreationPk']
    ), responses={status.HTTP_200_OK: teamRecreationScrapSerializer})
    def post(self, request):
        try:
            teamToken = request.data['teamToken']
            recreationPk = request.data['recreationPk']
            tSpace = teamSpace.objects.get(teamToken=teamToken)
            recreation = recreationMain.objects.get(pk=recreationPk)

            # 이미 해당 Recreation과 tSpace에 대한 teamRecreationScrap 객체가 존재하는지 확인
            existing_scrap = teamRecreationScrap.objects.filter(recreation=recreation, teamSpace=tSpace).first()
            if existing_scrap:
                existing_scrap.delete()  # 이미 존재할 경우 해당 객체 삭제
                return Response({"result": True, "message": "Scrap deleted."}, status=status.HTTP_200_OK)

            tRecreationScrap = teamRecreationScrap.objects.create(recreation=recreation, teamSpace=tSpace)
            serializer = teamRecreationScrapSerializer(tRecreationScrap)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except KeyError:
            return Response({"error": "Required data not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        except teamSpace.DoesNotExist:
            return Response({"error": "Teamspace not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except recreationMain.DoesNotExist:
            return Response({"error": "Recreation not found."}, status=status.HTTP_404_NOT_FOUND)

class teamSpaceRecreationScrapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: teamScrapListSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='recreationPk',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='헤더에 token 추가 및 params에 recreationPk 추가',
            )
        ]
    )
    def get(self, request):
        try:
            recreationPk = request.GET.get('recreationPk')
            recreation = recreationMain.objects.get(pk=recreationPk)

            tUsers = teamUser.objects.filter(user=request.user)
            teamList = [tUser.teamSpace for tUser in tUsers]

            scrapedRecreations = teamRecreationScrap.objects.filter(recreation=recreation, teamSpace__in=teamList)
            scrapedTeam = [scrapedRecreation.teamSpace for scrapedRecreation in scrapedRecreations]

            serializer = teamScrapListSerializer(teamList, many=True, context={'scrapedTeam': scrapedTeam})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except recreationMain.DoesNotExist:
            return Response({'error': 'Recreation not found'}, status=status.HTTP_404_NOT_FOUND)
        except teamUser.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class teamSpaceShoppingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,  # 리스트 형태로 요청 받음
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'teamToken': openapi.Schema(type=openapi.TYPE_STRING),
                    'item': openapi.Schema(type=openapi.TYPE_STRING),
                    'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
                required=['teamToken', 'item', 'price', 'amount'],
            ),
        )
    )
    def post(self, request):
        try:
            teamToken = request.data[0]['teamToken']
            tSpace = teamSpace.objects.get(teamToken=teamToken)
            shoppingList = teamShoppingScrap.objects.filter(teamSpace=tSpace)
            for shopping in shoppingList:
                shopping.delete()
            serializer = createTeamShoppingSerializer(data=request.data, context={'tSpace': tSpace}, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
        except teamSpace.DoesNotExist:
            return Response({'error': 'Invalid team token'}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: teamShoppingScrapSerializer})
    def get(self, request):
        try:
            teamToken = request.GET.get('teamToken')
            tSpace = teamSpace.objects.get(teamToken=teamToken)
            tShoppingScraps = teamShoppingScrap.objects.filter(teamSpace=tSpace)
            serializer = teamShoppingScrapSerializer(tShoppingScraps, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except teamSpace.DoesNotExist:
            return Response({'error': 'Invalid team token'}, status=status.HTTP_400_BAD_REQUEST)