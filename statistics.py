"""
For math and statistics calculations, showing graphs and etc...
This is in a strong relationship with Profiler to enhance the outcomes of experiments.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

from plotly.offline import plot
import plotly.graph_objs as objs
import profiler
import os

def DrawTree(evaluatedTree, controllerTitle):

    positions = []
    edges = []
    labels = []

    bottom = evaluatedTree.GetBottom()
    depth = bottom.depth

    currentDepthNodes = evaluatedTree.GetDepthNodes(depth)
    priviouseNodesCount = 0

    for i in range(len(currentDepthNodes)):
        positions.append((i, -1 * depth))
        labels.append(str(currentDepthNodes[i].point))

    while (depth > 0):
        parents = []
        previouseParent = None
        children = []
        # Finding the parent
        for i in range(len(currentDepthNodes)):
            if(previouseParent == None):
                previouseParent = currentDepthNodes[i].parent

            if currentDepthNodes[i].parent == previouseParent and i != len(currentDepthNodes) -1:
                children.append(positions[i + priviouseNodesCount])
            else:
                if(i == len(currentDepthNodes) -1):
                    children.append(positions[i + priviouseNodesCount])

                if(len(children) > 0):
                    parents.append(previouseParent)
                    xParent = sum(children[k][0] for k in range(len(children)))/len(children)
                    yParent = -1 * depth + 1
                    positions.append((xParent, yParent))
                    labels.append(str(previouseParent.point))

                    # Edges
                    for child in children:
                        edges += [((xParent, yParent),(child[0], child[1]))]

                    previouseParent = currentDepthNodes[i].parent

                children = []
                children.append(positions[i + priviouseNodesCount])
                if(i == len(currentDepthNodes) -1):
                    previouseParent = None
        priviouseNodesCount += len(currentDepthNodes)
        currentDepthNodes = parents
        parents = []

        depth -= 1


    xPositions = [positions[k][0] for k in range(len(positions))]
    yPositions = [positions[k][1] for k in range(len(positions))]

    xEdges = []
    yEdges = []

    for edge in edges:
        xEdges += [edge[0][0] , edge[1][0], None]
        yEdges += [edge[0][1] , edge[1][1], None] 


    index = 0
    nodes = objs.Scatter(
        x = xPositions,
        y = yPositions,
        text = labels,
        mode = 'markers',
        marker = dict(
            symbol = 'square-dot',
            size = 18, 
            color = '#6175c1',    #'#DB4551', 
            line = dict(color = 'rgb(50,50,50)', width = 1)
            ),
        hoverinfo = 'text',
        opacity = 0.8,
        name = 'nodes'
    )

    lines = objs.Scatter(
        x = xEdges,
        y = yEdges,
        mode = 'lines',
        line = dict(
            color = 'rgb(210,210,210)',
            width = 1),
        hoverinfo = 'none',
        name = 'edges'
    )

    xAxisData = dict(
        showline = False,
        zeroline = False,
        showgrid = False,
        showticklabels = False,
        )

    yAxisData = dict(
        showline = True,
        zeroline = False,
        showgrid = True,
        showticklabels = True,
        )

    layoutData = dict(
        title= 'Action Tree for {0} (Node counts: {1})'.format(controllerTitle, len(positions)),  
        xaxis = objs.XAxis(xAxisData),
        yaxis = objs.YAxis(yAxisData),  
        annotations = MakeAnnotations(positions, labels))
   
    data = objs.Data([nodes, lines])

    figure = dict (data=data, layout = layoutData)

    os.makedirs(profiler.RESULTPATH, exist_ok=True)
    plot(figure, filename='{0}/Action Tree for {1}.html'.format(profiler.RESULTPATH, controllerTitle))


def MakeAnnotations(positions, texts, font_size = 10, font_color = 'rgb(250,250,250)'):
    posLength = len(positions)
    textLength = len(texts)
    if(posLength != textLength):
        raise ValueError('Position and texts mismatch.')
    annotations = objs.Annotations()
    for k in range(posLength):
        currentColor = font_color
        currentText = texts[k]
        if(texts[k] == "None"):
            currentText = "X"
            currentColor = "red"
        annotations.append(
            objs.Annotation(
                text = currentText, 
                x = positions[k][0],
                y = positions[k][1],
                xref = 'x1',
                yref = 'y1',
                font = dict(color = currentColor, size = font_size),
                showarrow = False)
        )
    return annotations  


def DrawComparison(previouseProfileData, currentProfileData, type):
    """
    Draw comparison graph for these two profile data, with give type.
    type -> 1 is time, 2 is space and 3 is basic
    """

    AutoOpen = False

    #region for Basic Comparison -> 3
    # This trace represent total calls for both algorithms
    totalCallsTrace = objs.Bar(
            x = ['1) ' + previouseProfileData.Title, '2) ' + currentProfileData.Title],
            y = [int(previouseProfileData.TotalCalls), int(currentProfileData.TotalCalls)],
            name = 'Total Calls',
            marker = dict(
                color = 'rgb(55, 83, 109)'
            )
        )
    # This trace represent Algorithm calls for both algorithms
    algorithmCallsTrace = objs.Bar(
            x = ['1) ' + previouseProfileData.Title, '2) ' + currentProfileData.Title],
            y = [int(previouseProfileData.AlgorithmCalls), int(currentProfileData.AlgorithmCalls)],
            name = 'Algorithm Calls',
            marker = dict(
                color = 'rgb(26, 118, 255)'
            )
        )
    # This trace represent Neighbors calls for both algorithms
    neighborsCallsTrace = objs.Bar(
            x = ['1) ' + previouseProfileData.Title, '2) ' + currentProfileData.Title],
            y = [int(previouseProfileData.NeibursCount), int(currentProfileData.NeibursCount)],
            name = 'Neighbors Calls',
            marker = dict(
                color = 'rgb(126, 118, 255)'
            )
        )
    # This trace represent Evaluattion Calls for both algorithms
    EvaluattionCallsTrace = objs.Bar(
            x = ['1) ' + previouseProfileData.Title, '2) ' + currentProfileData.Title],
            y = [int(previouseProfileData.EvaluatedCount), int(currentProfileData.EvaluatedCount)],
            name = 'Evaluation Calls',
            marker = dict(
                color = 'rgb(200, 118, 255)'
            )
        )

    # Layout of the whole graph and data
    data = [totalCallsTrace, algorithmCallsTrace, neighborsCallsTrace, EvaluattionCallsTrace]
    layout = objs.Layout(
        title = 'Basic comparision for algorithms in calls counts!',
        xaxis = dict(
            title = 'Algorithms',
            tickfont = dict(
                size = 20,
                color = 'rgb(107, 107, 107)'
            )
        ),
        yaxis = dict(
            title = 'Count of calls',
            titlefont = dict(
                size = 16,
                color = 'rgb(107, 107, 107)'
        ),
        tickfont = dict(
            size = 15,
            color = 'rgb(107, 107, 107)'
            )
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor = 'rgba(255, 255, 255, 0)',
            bordercolor = 'rgba(255, 255, 255, 0)'
        ),
        barmode = 'group',
        bargap = 0.15,
        bargroupgap = 0.1
    )

    if (type == 3):
        AutoOpen = True
    else: 
        AutoOpen = False

    fig = objs.Figure(data=data, layout=layout)
    os.makedirs(profiler.RESULTPATH, exist_ok=True)
    plot(fig, auto_open = AutoOpen, filename = '{0}/{1} vs {2} - Basic Comparison.html'.format(profiler.RESULTPATH, previouseProfileData.Title, currentProfileData.Title))
    #endregion

    #region for Space Comparison -> 2
    # This trace represent Algorithm Recursive Container
    AlgorithmRecursiveTrace = objs.Bar(
            y = ['1) ' +previouseProfileData.Title, '2) ' +currentProfileData.Title],
            x = [int(previouseProfileData.AlgorithmRecursice), int(currentProfileData.AlgorithmRecursice)],
            name = 'Algorithm Recursive containter',
            orientation = 'h',
            marker = dict(
                color = 'rgba(246, 78, 139, 0.6)',
                line = dict(
                    color = 'rgba(246, 78, 139, 1.0)',
                    width = 3)
            )
        )

    # Represent copy counts of algorithms
    CopyCountTrace = objs.Bar(
        y = ['1) ' +previouseProfileData.Title, '2) ' +currentProfileData.Title],
        x = [int(previouseProfileData.CopyCount), int(currentProfileData.CopyCount)],
        name = 'Copy Count',
        orientation = 'h',
        marker = dict(
            color = 'rgba(58, 71, 80, 0.6)',
            line = dict(
                    color = 'rgba(58, 71, 80, 1.0)',
                    width = 3)
            )
        )

    # Represent Queue count of algorithms
    QueueCountTrace = objs.Bar(
            y = ['1) ' +previouseProfileData.Title, '2) ' +currentProfileData.Title],
            x = [int(previouseProfileData.QueueCount), int(currentProfileData.QueueCount)],
            name = 'Queue Count',
            orientation = 'h',
            marker = dict(
                color = 'rgba(74, 112, 74, 0.6)',
                line = dict(
                    color = 'rgba(74, 112, 74, 1.0)',
                    width = 3)
                )
            )

    # Represent Evaluation Container for algorithms
    EvaluationContainerTrace = objs.Bar(
        y = ['1) ' +previouseProfileData.Title, '2) ' +currentProfileData.Title],
        x = [int(previouseProfileData.EvaluatedCount), int(currentProfileData.EvaluatedCount)],
        name='Evelate Countainer',
        orientation = 'h',
        marker = dict(
            color = 'rgba(43, 103, 198, 0.6)',
            line = dict(
                color = 'rgba(43, 103, 198, 1.0)',
                width = 3)
            )
        )

    data = [AlgorithmRecursiveTrace, CopyCountTrace, QueueCountTrace, EvaluationContainerTrace]
    layout = objs.Layout(
        barmode = 'stack',
        title = 'Space comparision, which takes more memory in short!',
        xaxis = dict(
            title = 'Number of instances in Memory',
            tickfont = dict(
                size = 20,
                color = 'rgb(107, 107, 107)'
            )
        ),
        yaxis = dict(
            title = 'Algorithms',
            titlefont = dict(
                size = 16,
                color = 'rgb(107, 107, 107)'
         )
    ))

    if (type == 2):
        AutoOpen = True
    else: 
        AutoOpen = False

    fig = objs.Figure(data=data, layout=layout)
    os.makedirs(profiler.RESULTPATH, exist_ok=True)
    plot(fig, auto_open = AutoOpen, filename = '{0}/{1} vs {2} - Space Comparison.html'.format(profiler.RESULTPATH, previouseProfileData.Title, currentProfileData.Title))
    #endregion

    #region for Time Comparison -> 1
    # This trace represent timings of the first algorithm
    FirstAlgorithmTrace = objs.Scatter(
        name = previouseProfileData.Title,
        x = ["Total Time", "Evaluation Time" , "Algorithm Cumlative Time", "Call Time"],
        y = [previouseProfileData.TotalTime, 
            previouseProfileData.EvaluatedTime,
            previouseProfileData.AlgorithmCum,
            previouseProfileData.AlgorithmTime],
        fill = 'tozeroy'
    )
        
    # This trace represent timings of the second algorithm
    SecondAlgorithmTrace = objs.Scatter(
        name = currentProfileData.Title,
        x = ["Total Time", "Evaluation Time" , "Algorithm Cumlative Time", "Call Time"],
        y = [currentProfileData.TotalTime, 
            currentProfileData.EvaluatedTime,
            currentProfileData.AlgorithmCum,
            currentProfileData.AlgorithmTime],
        fill = 'tonexty'
    )

    layout = objs.Layout(
        title = 'Time comparison between algorithms',
        xaxis = dict(
            title = 'Time Measures',
            tickfont = dict(
                size = 20,
                color = 'rgb(107, 107, 107)'
            )
        ),
        yaxis = dict(
            title = 'Time spent in seconds',
            titlefont = dict(
                size = 16,
                color = 'rgb(107, 107, 107)'
        ))
    )

    data = [FirstAlgorithmTrace, SecondAlgorithmTrace]

    if (type == 1):
        AutoOpen = True
    else: 
        AutoOpen = False

    fig = objs.Figure(data = data, layout = layout)
    os.makedirs(profiler.RESULTPATH, exist_ok=True)
    plot(fig, auto_open = AutoOpen, filename = '{0}/{1} vs {2} - Time Comparison.html'.format(profiler.RESULTPATH, previouseProfileData.Title, currentProfileData.Title))
    #endregion
