from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from media_app.models import MediaFile
from media_app.forms import MediaFileForm
from django.http import HttpResponseForbidden
import os

@login_required
def media_list(request):
    media_files = MediaFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request,'media_app/media_list.html', {'media_files': media_files})



@login_required

def media_upload(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('media_app:media_list')
    else:
        form = MediaFileForm()
    return render(request, 'media_app/media_form.html', {'form': form})


@login_required
def media_edit(request,pk):
    media_file = get_object_or_404(MediaFile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media_file)
        if form.is_valid():
            
            form.save()  
            return redirect('media_app:media_list')
    else:
        form = MediaFileForm(instance=media_file)
    return render(request, 'media_app/media_form.html', {'form': form})

@login_required

def media_delete(request,pk):
    media_file = get_object_or_404(MediaFile, pk=pk, user=request.user)
    if media_file.user != request.user:
        return HttpResponseForbidden("You can't delete this media file.")
    if media_file.file:
        if os.path.isfile(media_file.file.path):
            os.remove(media_file.file.path)

    media_file.delete()
    return redirect('media_app:media_list')