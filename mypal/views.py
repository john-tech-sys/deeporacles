import openai
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from deeporacles.settings import OPENAI_KEY
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Conversation
from .forms import MessageForm
from mypal.models import Message


@csrf_exempt
def generate_response(request):
    """
    Generates a response based on the user input using GPT-3 and returns it as a JSON response.
    """
    if request.method == 'POST':
        # Retrieve user input from request
        user_input = request.POST.get('input_text')

        # Check if user input is provided
        if not user_input:
            return JsonResponse({'error': 'Input text is required'}, status=400)

        try:
            # Set your OpenAI API key
            openai.api_key = OPENAI_KEY

            # Generate response using GPT-3
            response = openai.Completion.create(
                engine="text-davinci-002",  # Select GPT-3 engine
                prompt=user_input,  # Input prompt
                max_tokens=100,  # Maximum length of generated response
                n=1,  # Number of response samples to generate
                stop=None  # Stop sequence to end the generation
            )

            # Extract the generated response text from the API response
            generated_text = response.choices[0].text.strip()

            # Return the generated response as JSON
            return JsonResponse({'response': generated_text})
        
        except openai.error.OpenAIError as e:
            # Handle OpenAI API errors
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


@login_required
def conversation_detail(request, conversation_id):
    """
    Renders the details of a conversation based on the provided conversation_id.

    Parameters:
        request: HttpRequest object containing metadata about the request
        conversation_id: int representing the ID of the conversation to display

    Returns:
        HttpResponse with the rendered conversation details
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages_qs = conversation.messages.all().order_by('timestamp')
    message_form = MessageForm()

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.conversation = conversation
            new_message.user = request.user
            new_message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('conversation_detail', conversation_id=conversation_id)
        else:
            messages.error(request, 'Failed to send message. Please check the form.')

    return render(request, 'conversation_detail.html', {
        'conversation': conversation,
        'messages': messages_qs,
        'message_form': message_form
    })


# def mypal(request):
#     """
#     A view function that handles POST requests to create messages using OpenAI, save them, and 
#     render the message creation page with the updated context. Handles form validation, error 
#     handling, message generation, and rendering of the message creation page. Returns the rendered 
#     page with messages and the form. 
#     """
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             input_text = form.cleaned_data['user_input']
#             try:
#                 openai.api_key = OPENAI_KEY
#                 response = openai.Completion.create(
#                     engine="text-davinci-002",
#                     prompt=input_text,
#                     max_tokens=100,
#                     n=1,
#                     stop=None
#                 )
#                 generated_text = response.choices[0].text.strip()
#                 new_message = form.save(commit=False)
#                 new_message.message = generated_text
#                 new_message.user = request.user  # Attach the user to the message
#                 new_message.save()
#                 messages = Message.objects.all()  # Retrieve all messages
#                 context = {'messages': messages, 'form': form}
#                 return render(request, 'mypal/create_message.html', context)
#             except Exception as e:
#                 error_message = str(e)
#                 return render(request, 'mypal/create_message.html', {'error': error_message})
#         else:
#             # Form is invalid, render the page with the form and error messages
#             messages = Message.objects.all()  # Retrieve all messages
#             return render(request, 'mypal/create_message.html', {'messages': messages, 'form': form})
    
#     # If the request method is not POST, render the page with an empty form
#     form = MessageForm()
#     messages = Message.objects.all()  # Retrieve all messages
#     context = {'messages': messages, 'form': form}
#     return render(request, 'mypal/create_message.html', context)


openai.api_key = OPENAI_KEY

# this is the home view for handling home page logic
@login_required
def mypal(request):
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "Mypal", "content": "I am still under development, I will be ready to interact with you soon. I highly appreciate you petience. For any questions you can contact the Admin of Deep Oracles"},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'mypal/create_message.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'mypal/create_message.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('404')


def mypals(request):
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Define your chatbot's predefined prompts
        prompts = []

        # Append user input to the conversation
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Append conversation messages to prompts
        prompts.extend(conversation)

        # Set up and invoke the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompts,
            api_key=OPENAI_KEY
        )
        
        # Extract chatbot replies from the response

        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        request.session['conversation'] = conversation

        return render(request, 'mypal/create_message.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        request.session.clear()
        return render(request, 'mypal/create_message.html', {'conversation': conversation})



@login_required
def list_conversations(request: HttpRequest) -> HttpResponse:
    """
    List all conversations for the current user.

    Arguments:
        request: Django HttpRequest object containing metadata about the request

    Returns:
        HttpResponse with the rendered list of conversations
    """
    conversations = Conversation.objects.filter(user=request.user).order_by('-timestamp')
    context = {'conversations': conversations}
    return render(request, 'conversation_list.html', context)



@require_POST
def delete_conversation(request, conversation_id):
    """Delete a conversation if the user is the owner."""
    conversation = Conversation.objects.filter(id=conversation_id, user=request.user).first()
    if conversation:
        conversation.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Conversation not found or you do not have permission to delete it.'}, status=404)

