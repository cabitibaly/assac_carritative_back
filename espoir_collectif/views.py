from django.db import IntegrityError
from .models  import *
from rest_framework import status
from rest_framework.decorators import api_view ,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
from django.contrib.auth import get_user_model



@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'message': 'Tous les champs sont obligatoires'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'message': 'Un utilisateur avec cet email existe déjà'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({'message': 'Inscription réussie', 'status': 201}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'message': str(e), 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_message)
    
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'message': 'L\'email et le mot de passe sont obligatoires'}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
         return Response({'message': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)


    user = authenticate(request, username=user.username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Connexion réussie', 'token': token.key, 'status': 200}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Email ou mot de passe incorrectes', 'status': 401}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):

    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Déconnexion réussie', 'status': 200}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'message': 'Ooops, quelque chose s\'est mal passé', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_message)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUser(request):
    try:
        user = User.objects.get(id=request.user.id)
        data = {
            'username': user.username,
            'email': user.email
        }
        return Response({'user': data, 'status': 200}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'Utilisateur non trouvé', 'status': 404}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUser(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password_old = request.data.get('passwordOld')
    password_new = request.data.get('passwordNew')

    if password_old and not password_new:
        return Response({'message': 'Veuillez renseigner le nouveau mot de passe', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

    if password_old != '':
        try:
            user = User.objects.get(id=request.user.id)
        
            if not user.check_password(password_old):
                return Response({'message': 'L\'ancien mot de passe est incorrect', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
            user.username = username
            user.email = email
            user.set_password(password_new)
            user.save()
            return Response({'message': 'Utilisateur modifié avec succès', 'status': 200}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Utilisateur non trouvé', 'status': 404}, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            user = User.objects.get(id=request.user.id)
        
            user.username = username
            user.email = email
            user.save()
            return Response({'message': 'Utilisateur modifié avec succès', 'status': 200}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Utilisateur non trouvé', 'status': 404}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'message': 'Veuillez renseigner correctemet les informations', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def creer_cagnotte(request):
    intitule = request.data.get('intitule')
    description = request.data.get('description')
    objectif_montant_vise = request.data.get('objectif')
    image = request.FILES.get('img') 
    
    if not intitule or not description or not objectif_montant_vise:
        return Response({'message': 'Tous les champs obligatoires doivent être renseignés', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cagnotte = Cagnotte.objects.create(
            intitule=intitule,
            description=description,
            objectif_montant_vise=objectif_montant_vise,
            date_debut=datetime.now(),
            image=image,
            montant_collecte=0,
            created_by=request.user
        )
        return Response({'message': 'Cagnotte créée avec succès', 'status': 201}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'message': str(e), 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_message)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def details_cagnotte(request, cagnotte_id):
    try:
        cagnotte = Cagnotte.objects.get(id=cagnotte_id)
    except Cagnotte.DoesNotExist:
        return Response({'message': 'Cagnotte non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    cagnotte_details = {
        'intitule': cagnotte.intitule,
        'description': cagnotte.description,
        'objectif_montant_vise': cagnotte.objectif_montant_vise,
        'montant_collecte': cagnotte.montant_collecte,
        'date_debut': cagnotte.date_debut,
        'image': cagnotte.image.url if cagnotte.image else None,
        'organisateur': cagnotte.created_by.username
    }

    dons = Don.objects.filter(cagnotte=cagnotte)
    dons_list = [
        {
            'montant': don.montant,
            'nom_donateur': don.donateur.nom if don.donateur else None,
            'message_donateur': don.donateur.message if don.donateur else None,
        }
        for don in dons
    ]

    return Response({
        'cagnotte': cagnotte_details,
        'dons': dons_list,
        'status': 200
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_cagnottes(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return Response({'message': 'Utilisateur non trouvé', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

    try:
        cagnottes = Cagnotte.objects.filter(created_by=user)
        data = [
            {
                'id': cagnotte.id,
                'intitule': cagnotte.intitule,
                'image_url': cagnotte.image.url if cagnotte.image else None,
            }
            for cagnotte in cagnottes
        ]
        return Response({'message': data, 'status': 200}, status=status.HTTP_200_OK)   
    except Cagnotte.DoesNotExist:
        return Response({'message': 'Aucune cagnotte trouvée', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def liste_cagnottes(request):

    try:
        cagnottes = Cagnotte.objects.all()
    except Cagnotte.DoesNotExist:
        return Response({'message': 'Aucune cagnotte trouvée'}, status=status.HTTP_404_NOT_FOUND)
    
    data = [
        {
            'id': cagnotte.id,
            'intitule': cagnotte.intitule,
            'description': cagnotte.description,
            'montant_collecte': cagnotte.montant_collecte,
            'objectif_montant_vise': cagnotte.objectif_montant_vise,
            'date_debut': cagnotte.date_debut,
            'image_url': cagnotte.image.url if cagnotte.image else None,
            'created_by': cagnotte.created_by.username
        }
        for cagnotte in cagnottes
    ]
    return Response({'message': data, 'status': 200}, status=status.HTTP_200_OK)  
  
@api_view(['GET'])
def rechercher_cagnotte(request, terme):
    try:
        cagnottes = Cagnotte.objects.filter(intitule__icontains=terme)
    except Cagnotte.DoesNotExist:
        return Response({'message': 'Aucune cagnotte trouvée'}, status=status.HTTP_404_NOT_FOUND)
    
    data = [
        {
            'id': cagnotte.id,
            'intitule': cagnotte.intitule,
            'description': cagnotte.description,
            'montant_collecte': cagnotte.montant_collecte,
            'objectif_montant_vise': cagnotte.objectif_montant_vise,
            'date_debut': cagnotte.date_debut,
            'image_url': cagnotte.image.url if cagnotte.image else None,
            'created_by': cagnotte.created_by.username
        }
        for cagnotte in cagnottes
    ]
    return Response({'message' : data, 'status': 200}, status=status.HTTP_200_OK)

@api_view(['POST'])
def faire_don(request, cagnotte_id):
    cagnotte_id = request.data.get('id')
    montant = request.data.get('montant')
    nom = request.data.get('nom')
    message = request.data.get('message')
    email = request.data.get('email')

    print(cagnotte_id, montant, nom, message, email)

    if not cagnotte_id or not montant or not nom:
        return Response({'message': 'Tous les champs sont requis', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cagnotte = Cagnotte.objects.get(id=cagnotte_id)
    except Cagnotte.DoesNotExist:
        return Response({'message': 'Cagnotte non trouvée', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

    
    donateur, created = Donateur.objects.get_or_create(
        nom=nom,
        message=message,
        email=email
    )


    don = Don.objects.create(
        montant=montant,
        cagnotte=cagnotte,
        donateur=donateur,
    )

    cagnotte.montant_collecte += montant
    cagnotte.save()

    return Response({'message': 'Don effectué avec succès', 'status': 201}, status=status.HTTP_201_CREATED)
