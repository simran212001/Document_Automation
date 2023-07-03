from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import Context,UseCase
def home1(request):
    return render(request,'home1.html')


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
    G.add_node(actor, shape="v", color='green', style='filled', pos=(0, 0))
    G.add_node(action, shape="d", color='lightblue', style='filled', pos=(1, 0))
    i = len(fields)
    i = int(i/2)
    for field in fields:
        print(i)
        G.add_node(field, shape="o", color='yellow', style='filled', pos=(2, i))
        G.add_edge(action, field)
        G.add_edge(actor, action)
        i = i - 1
    pos = nx.get_node_attributes(G, 'pos')

    plt.figure(figsize=(16, 8))
    plt.clf()

    for node in G.nodes(data=True):
        shape = node[1]['shape']
        color = node[1]['color']
        nx.draw_networkx_nodes(G, pos, nodelist=[node[0]], node_shape=shape, node_color=color, node_size=3000)  # Increase node_size
    
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
        fields = request.POST.get('fields')

        fields = [field.strip() for field in fields.split(',')]  # Split the input by comma and remove leading/trailing spaces

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

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template import loader
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import PDFReport, UploadedImage
from django.http import HttpResponse
from django.views import View
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Context, PDFReport
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

class GeneratePDF(View):
    def get(self, request, pdf_report_id=None):
        if pdf_report_id is not None:
            try:
                pdf_report = PDFReport.objects.get(id=pdf_report_id)
            except PDFReport.DoesNotExist:
                return HttpResponse("Invalid PDF report ID")

            objective = pdf_report.objective
            scope = pdf_report.scope
            overview = pdf_report.overview
            context_diagrams = pdf_report.context_diagrams.all()
            use_case_diagrams = pdf_report.use_case_diagrams.all()

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            objective_heading_style = styles['Heading1']
            objective_content_style = styles['BodyText']

            # Render the objective heading with content
            elements.append(Paragraph("Purpose:", objective_heading_style))
            elements.append(Paragraph(objective, objective_content_style))
            elements.append(Spacer(1, 12))

            elements.append(Paragraph("Scope:", objective_heading_style))
            elements.append(Paragraph(scope, objective_content_style))
            elements.append(Spacer(1, 12))

            elements.append(Paragraph("Overview:", objective_heading_style))
            elements.append(Paragraph(overview, objective_content_style))
            elements.append(Spacer(1, 12))

            # Add context diagram images
            elements.append(Paragraph("Context Diagrams:", objective_heading_style))
            for context_diagram in context_diagrams:
                context_img = Image(context_diagram.image.path, width=400, height=300)
                elements.append(context_img)
                elements.append(Spacer(1, 12))

            # Add use case diagram images
            elements.append(Paragraph("Use Case Diagrams:", objective_heading_style))
            for use_case_diagram in use_case_diagrams:
                use_case_img = Image(use_case_diagram.image.path, width=400, height=300)
                elements.append(use_case_img)
                elements.append(Spacer(1, 12))

            doc.build(elements)

            buffer.seek(0)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            response.write(buffer.getvalue())

            return response

        else:
            # Retrieve the title from the Context model
            try:
                context = Context.objects.latest('id')
                title = context.srs_name
            except Context.DoesNotExist:
                title = ""

            # Create a file-like buffer to receive PDF data
            buffer = BytesIO()

            # Create the PDF object, using the buffer as its "file"
            p = canvas.Canvas(buffer)

            # Set font and font size
            p.setFont("Helvetica", 12)

            # Set page size
            p.setPageSize((595, 842))  # A4 size: 595x842 points

            # Set the top margin for the page
            top_margin = 750

            # Write the company details
            p.drawString(50, top_margin, "Engineering Innovations Research Lab P Ltd")
            p.drawString(50, top_margin - 15, "2004/C, Vijay Nagar, Near SBI Chowk")
            p.drawString(50, top_margin - 30, "Jabalpur, MP 482002")
            p.drawString(50, top_margin - 45, "(+91) 951-670-3294")

            # Set the title and subtitle
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, top_margin - 90, title)
            p.setFont("Helvetica", 12)
            p.drawString(50, top_margin - 120, "LIVE TRACKING OF BUS Project")
            p.setFont("Helvetica-Bold", 14)
            p.drawString(50, top_margin - 170, "INDEX")
            # ... continue with the rest of the PDF content ...

            # Save the PDF document
            p.showPage()
            p.save()

            # File buffer rewind
            buffer.seek(0)

            # Set the return type of the response as a PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # Write the PDF buffer to the response
            response.write(buffer.getvalue())

            return response


def generate_pdf(request):
    if request.method == 'POST':
        objective = request.POST.get('objective')
        scope = request.POST.get('scope')
        overview = request.POST.get('overview')
        context_diagrams = request.FILES.getlist('context_diagrams')
        use_case_diagrams = request.FILES.getlist('use_case_diagrams')
        
        # Save the form data to the database
        pdf_report = PDFReport(objective=objective, scope=scope, overview=overview)
        pdf_report.save()

        for diagram in context_diagrams:
            uploaded_image = UploadedImage(image=diagram)
            uploaded_image.save()
            pdf_report.context_diagrams.add(uploaded_image)

        for diagram in use_case_diagrams:
            uploaded_image = UploadedImage(image=diagram)
            uploaded_image.save()
            pdf_report.use_case_diagrams.add(uploaded_image)

        # Redirect to the PDF generation view
        return redirect('generate_pdf', pdf_report_id=pdf_report.id)
    
    return render(request, 'Generate_file.html')



# from django.shortcuts import render, redirect
# from .models import Process, DataFlow, DataStore

# def generate_dfd(request):
#     if request.method == 'POST':
#         # Get form data
#         process_name = request.POST.get('process_name')
#         data_flow_name = request.POST.get('data_flow_name')
#         source_process_id = request.POST.get('source_process')
#         target_process_id = request.POST.get('target_process')
#         data_store_name = request.POST.get('data_store_name')

#         # Create and save the objects
#         process = Process(name=process_name)
#         process.save()

#         data_flow = DataFlow(name=data_flow_name,
#                              source_id=source_process_id,
#                              target_id=target_process_id)
#         data_flow.save()

#         data_store = DataStore(name=data_store_name)
#         data_store.save()

#         # Redirect back to the DFD generation page
#         return redirect('generate_dfd')

#     # Render the DFD generation page with existing data
#     processes = Process.objects.all()
#     data_flows = DataFlow.objects.all()
#     data_stores = DataStore.objects.all()

#     context = {
#         'processes': processes,
#         'data_flows': data_flows,
#         'data_stores': data_stores,
#     }

#     return render(request, 'dfd_template.html', context)

import pygraphviz as pgv
from django.http import HttpResponse

def generate_dfd(request):
    # Create a new graph
    graph = pgv.AGraph(directed=True)

    # Define the nodes (entities and processes)
    entities = ['Entity A', 'Entity B']
    processes = ['Process 1', 'Process 2', 'Process 3']

    # Add the nodes to the graph
    for entity in entities:
        graph.add_node(entity, shape='box')

    for process in processes:
        graph.add_node(process, shape='ellipse')

    # Define the data flows and their connections
    data_flows = [
        ('Entity A', 'Process 1'),
        ('Process 1', 'Process 2'),
        ('Process 1', 'Entity B'),
        ('Process 2', 'Process 3'),
        ('Process 3', 'Entity B'),
    ]

    # Add the edges (connections) to the graph
    for source, target in data_flows:
        graph.add_edge(source, target)

    # Set the layout algorithm for the graph
    graph.layout(prog='dot')

    # Save the graph as an image
    diagram_path = 'path/to/your/dfddiagram.png'
    graph.draw(diagram_path)

    # Open the image and return it as an HTTP response
    with open(diagram_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/png')

    return response
