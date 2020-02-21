# Replace All Phone with phones

# -------------------------------------------------------
# Remove image from stakeholder.create
# Add after
if request.FILES.get('image'):
    Medical_Institutions.image = request.FILES.get('image')
    Medical_Institutions.save()
# -------------------------------------------------------
# inside if not stakeholder:
# Add User to django
user = User.objects.create_user(
    username=request.POST.get('national_number'),
    password=request.POST.get('password')
)

# Add user to the group
group = Group.objects.get(name='StakeholderType')
group.user_set.add(user)

# Remove password from stakeholder and add user=user

# --------------------------------------------------------
# Insert after the previous if condition
else:
    group = Group.objects.get(name='StakeholderType')
    group.user_set.add(stakeholder.user)
