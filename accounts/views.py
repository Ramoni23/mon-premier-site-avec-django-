from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate


User = get_user_model()
# recuperer la vue du formulaire dans signup.html
def signup(request): # inscrire l'utilisateur
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password) # creer l'utilisateur dans la bd
        login(request, user) # connecter notre utilisateur
        return redirect("index") # rediriger vers la vue d'accueil

    return render(request, 'accounts/signup.html')

# 
# connecter l'utilisateur
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # verifier que les infos envoyé sont bonnes et connecter l'utilisateur ou afficher un msg d'erreur
        user = authenticate(username=username, password=password) 
        if user:
            login(request, user)
            return redirect('index')
            
    return render(request, 'accounts/login.html')


def logout_user(request): # deconnecter l'utilisateur
    logout(request)
    return redirect('index')