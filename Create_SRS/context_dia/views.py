from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import Context,UseCase

def home(request):
    return render(request,'home.html')


def Context_dia(request):
    if request.method == 'POST':
        srs_name = request.POST.get('srs_name')
        print(srs_name)
        entities = request.POST.getlist('entities')
        print(len(entities))
        for i in range(len(entities)):
            print(entities[i])
        context = Context()
        context.srs_name = srs_name
        context.entities = entities
        context.save()
        print('Saved')
        graph = create_graph(srs_name,entities)  # call the create_graph function
        print('Saved and graph created')
        return render(request, 'Image.html', {'graph': graph})
    else:
        return render(request, 'context.html')

import networkx as nx
import matplotlib.pyplot as plt
import os
from django.conf import settings
import shutil

def create_graph(srs_name, entities):
    # create an empty graph
    G = nx.Graph()

    # add the center node
    G.add_node(srs_name)

    # add the external nodes
    for entity in entities:
        G.add_node(entity)

    # add edges between the center node and the external nodes
    for entity in entities:
        G.add_edge(srs_name, entity)

    # draw the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8))  # Set figure size to 8x8 inches
    plt.cla()  # Clear the current axes
    nx.draw_networkx_nodes(G, pos, nodelist=[srs_name], node_color='red', node_shape='o', node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=entities, node_color='blue', node_shape='o', node_size=1000)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=10, width=1)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

    image_path = os.path.join(settings.BASE_DIR, 'static', 'graph.png')

    plt.savefig(image_path)
    plt.show()

    copy_path = os.path.join(settings.BASE_DIR, 'static', 'copy_graph.png')
    shutil.copyfile(image_path, copy_path)

    print('copy')
    return '/static/graph.png'
 
import matplotlib
matplotlib.use('Agg')
def create_usecase(actor, action, fields):
    G = nx.DiGraph()
    G.add_node(actor, color='green', style='filled', pos=(0, 0))
    G.add_node(action, color='lightblue', style='filled', pos=(1, 0))
    i = len(fields)
    i = int(i/2)
    for field in fields:
        print(i)
        G.add_node(field, color='yellow', style='filled', pos=(2, i))
        G.add_edge(action, field)
        G.add_edge(actor, action)
        i = i-1
    pos = nx.get_node_attributes(G, 'pos')
    
    plt.figure(figsize=(8, 8))
    plt.clf()

    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=[node[1]['color'] for node in G.nodes(data=True)])
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)
    
    image_path = os.path.join(settings.BASE_DIR, 'static', 'usecase.png')
    plt.savefig(image_path)
    return '/static/usecase.png'


def UseCase_dia(request):
    if request.method == 'POST':
        actor = request.POST.get('actor')
        print(actor)
        action = request.POST.get('action')
        print(action)
        fields = request.POST.getlist('fields')
        for i in fields:
            print(i)
        if actor == 'other':
            actor = request.POST.get('actor-text')
        if action == 'other':
            action = request.POST.get('action-text')
        if 'other' in fields:
            fields = [request.POST.get('fields-text')]
        activity = UseCase(actor=actor, action=action, fields=fields)
        activity.save()
        graph = create_usecase(actor,action,fields)  # call the create_graph function
        print('Saved and graph created')
        return render(request, 'Image.html', {'graph': graph})
        # return render(request, 'UseCaseDia.html',{actor})
    else:
        return render(request, 'UseCase.html')


def ERD(request):
    return render(request,'ERD.html')







def notify(request):
    return render(request, 'Notification.html')


