from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Candidate, Position, Voter, Vote
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count






# Create your views here.
@login_required(login_url='login_view')
def home(request):
    return render(request, 'base/home.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_view')

    return render(request, 'base/login.html')



def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not email:
            messages.error(request, "email is required.")
            return redirect("register")
        
        if not username:
            messages.error(request, "registration number is required.")
            return redirect("register")


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Student with that registration number already exists, continue to login.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        Voter.objects.create(user=user)
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login_view")

    return render(request, "base/register.html")

    
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')


@login_required(login_url='login_view')
def voted(request):
    return render(request, 'base/voted.html')






@login_required(login_url='login_view')
def vote(request):
    # Get the voter's selected school
    voter = Voter.objects.filter(user=request.user).first()
    if not voter or not voter.school:
        messages.error(request, "You must select a school before voting.")
        return redirect('school_selection')

    if request.method == 'POST':
        # Iterate through the POST data to find selected candidates for each position
        for key, value in request.POST.items():
            if key.startswith('position_'):
                position_id = key.split('_')[1]  # Extract position ID from the key
                candidate_id = value  # Selected candidate ID

                # Ensure the candidate and position exist
                position = get_object_or_404(Position, id=position_id)
                candidate = get_object_or_404(Candidate, id=candidate_id)

                # Check if the voter has already voted for this position
                if Vote.objects.filter(voter=voter, position=position).exists():
                    messages.error(request, f"You have already voted.")
                    return redirect('vote')

                # Create a new vote
                Vote.objects.create(voter=voter, position=position, candidate=candidate)

        messages.success(request, "Your votes have been submitted successfully!")
        return redirect('voted')

    # Fetch all positions and their candidates, filtered by the voter's school
    positions = Position.objects.prefetch_related(
        models.Prefetch('candidates', queryset=Candidate.objects.filter(school=voter.school))
    ).all()
    context = {'positions': positions}
    return render(request, 'base/vote.html', context)







@login_required(login_url='login_view')
def vote(request):
    if request.method == 'POST':
        # Get the voter or create one if they don't exist
        voter, created = Voter.objects.get_or_create(user=request.user)

        # Iterate through the POST data to find selected candidates for each position
        for key, value in request.POST.items():
            if key.startswith('position_'):
                position_id = key.split('_')[1]  # Extract position ID from the key
                candidate_id = value  # Selected candidate ID

                # Ensure the candidate and position exist
                position = get_object_or_404(Position, id=position_id)
                candidate = get_object_or_404(Candidate, id=candidate_id)

                # Check if the voter has already voted for this position
                if Vote.objects.filter(voter=voter, position=position).exists():
                    messages.error(request, f"You have already voted.")
                    return redirect('vote')

                # Create a new vote
                Vote.objects.create(voter=voter, position=position, candidate=candidate)

        messages.error(request, "Your votes have been submitted successfully!")
        return redirect('voted')

    # Fetch all positions and their candidates
    positions = Position.objects.prefetch_related('candidates').all()
    context = {'positions': positions}
    return render(request, 'base/vote.html', context)

@login_required(login_url='login_view')
def review(request):
    voter = Voter.objects.filter(user=request.user).first()
    votes = Vote.objects.filter(voter=voter).select_related('position', 'candidate')
    context = {'votes': votes}
    return render(request, 'base/review.html', context)

@login_required(login_url='login_view')
def positions_list(request):
    # Fetch all positions
    positions = Position.objects.all()
    context = {'positions': positions}
    return render(request, 'base/seats.html', context)



@login_required(login_url='login_view')
def position_details(request, position_id):
    # Fetch the position and its candidates
    position = get_object_or_404(Position, id=position_id)
    candidates = position.candidates.all()
    context = {'position': position, 'candidates': candidates}
    return render(request, 'base/position_details.html', context)

@login_required(login_url='login_view')
def voting_status(request):
    # Fetch the current user's votes
    user_votes = Vote.objects.filter(voter__user=request.user).select_related('candidate', 'position')

    # Fetch vote counts for each candidate
    vote_counts = (
        Vote.objects.values('candidate__name')
        .annotate(total_votes=Count('candidate'))
        .order_by('-total_votes')
    )

    # Prepare data for the chart
    candidates = [item['candidate__name'] for item in vote_counts]
    votes = [item['total_votes'] for item in vote_counts]

    context = {
        'status': "Voted" if user_votes.exists() else "Not Voted",
        'user_votes': user_votes,
        'candidates': candidates,
        'votes': votes,
    }
    return render(request, 'base/status.html', context)




@login_required(login_url='login_view')
def spoiled_votes(request):
    # Define spoiled votes
    spoiled_votes = Vote.objects.filter(
        models.Q(candidate__isnull=True) |  # Votes with no candidate
        models.Q(position__isnull=True)     # Votes with no position
    )

    # Add logic to detect multiple votes by the same voter for the same position
    # (Optional, depending on your requirements)

    context = {
        'spoiled_votes': spoiled_votes,
    }
    return render(request, 'base/spoiled_votes.html', context)