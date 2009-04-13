/*
 * =====================================================================================
 *
 *       Filename:  _traverse.c
 *
 *    Description:  深度优先遍历二维地图 python 模块
 *
 *        Version:  1.0
 *        Created:  2009年04月13日 22时36分47秒 CST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:   yihuang(yi.codeplayer@gmail.com),
 *        Company:
 *
 * =====================================================================================
 */
#include "Python.h"

typedef struct _position
{
    int x,y;
    struct _position *next;
}Position;

=NULL;

void enqueue(Position **queue_head, int x, int y)
{
    Position *position = malloc(sizeof(*position));
    position->x = x;
    position->y = y;
    position->next = *queue_head;
    *queue_head = position;
    return;
}

Position *unqueue(Position **queue_head)
{
    if(*queue_head==NULL)
	return NULL;
    Position *result = *queue_head;
    if(queue_head!=NULL && *queue_head!=NULL)
	*queue_head = (*queue_head)->next;
    return result;
}

bool traverse(Position ***graph, int height, int width)
{
    Position *position = NULL, *visit_queue = NULL;
    // init visited map
    int **visited = malloc( height * sizeof(*visited) + height * width * sizeof(**visited) );
    memset(visited, 0,  height * sizeof(*visited) + height * width * sizeof(**visited) );
    int *tmp = (int *)visited+height;
    for(int i=0; i<height; i++)
    {
        visited[i] = tmp + i*width;
	for(int j=0; j<width; j++)
	{
	    visited[i][j] = 0;
	}
    }
    // init queue
    enqueue(&visit_queue, 0, 0);
    while(visit_queue)
    {
        position = unqueue(visit_queue);
	if(position.x==height-1 && position.y==width-1)
	    break;
	//TODO
    }
}

static PyObject *py_traverse(PyObject *self, PyObject *args)
{
    PyObject *py_graph, *py_graph_item, *py_position ;
    int height=0, width=0;
    int x=0, y=0;
    if (!PyArg_ParseTuple(args, "o", &py_graph))
        return NULL;
    if(py_graph==NULL || height==0 || width==0)
	goto invalid_arg;
    if(!PySequence_Check(py_graph) || (height=PySequence_Size(py_graph))<=0)
	goto invalid_arg;
    py_graph_item = PySequence_GetItem(py_graph, 0);
    if(py_graph_item==NULL || !PySequence_Check(py_graph_item) || (width = PySequence_Size(py_graph_item)==0)
        goto invalid_arg;
    py_position = PySequence_GetItem(py_graph_item, 0);
    if(py_position==NULL || !PySequence_Check(py_position) || PySequence_Size(py_position)!=2)
        goto invalid_arg;
    Position ***graph=malloc( height * sizeof(*graph) + height * width * sizeof(**graph) );
    Position **tmp = (Position **)(graph + height);
    /* init M*N 2-d array */
    for(int i=0; i<height; i++)
    {
	*(graph+i) = tmp+i*width;
	if(py_graph_item=PySequence_GetItem(py_graph, i)==NULL)
            goto invalid_arg;
	for(int j=0; j<width; j++)
	{
            PyObject *py_position = PySequence_GetItem(py_graph_item, j);
	    if (py_position==NULL || !PyArg_ParseTuple(py_position, "dd", &x, &y))
		goto invalid_arg;
            Position *position = malloc(sizeof(Position));
	    position->x = x;
	    position->y = y;
	    position->next = NULL;
	    graph[i][j] = position;
	}
    }
    bool connected = traverse(graph, height, width);
    PyObject *py_result = Py_BuildValue("b", connected);
    return py_result;
invalid_arg:
    // TODO set exception
    return NULL;
}

static PyMethodDef TraverseMethods[] = {
    ...
    {"traverse",  py_traverse, METH_VARARGS,
     "traverse a graph"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
init_traverse()
{
    PyObject *_module;

    _module = Py_InitModule("_traverse", TraverseMethods);
    if (_module == NULL)
    return;


}
