# Add in views
.filter(hide=False)
if request.method == 'POST':
    StakeholderType = get_object_or_none(StakeholderType, StakeholderTypeID=request.POST.get('id'))
    if StakeholderType:
        StakeholderType.hide = True
        StakeholderType.save()

# in the templates
# Add NN or id in table

# Delete
# Delete the button tag
'''
<a class="btn btn-danger btn-xs" onclick="delete_item({{doctor.physician_nn}})">
    <i class="fa fa-trash-o"></i>
</a>
'''
