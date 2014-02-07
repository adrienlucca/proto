from traits.api import HasTraits, Range, Instance, \
                    on_trait_change
from traitsui.api import View, Item, HGroup
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import \
                    MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

import tetgen, geometry
from pprint import pprint
import random,csv

all_colors = [(name, float(X), float(Y), float(Z))
              for name, X, Y, Z in csv.reader(open('data/XYZcolorlist.csv'))]
tg, hull_i = geometry.tetgen_of_hull([(X,Y,Z) for name, X, Y, Z in all_colors])
colors = [all_colors[i] for i in hull_i]

print ("thrown out: "
       + ", ".join(set(zip(*all_colors)[0]).difference(zip(*colors)[0])))

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    X = Range(0., 100., 0.)
    Y = Range(0.01, 100., 1.)
    Z = Range(0., 100., 0.)
    x = Range(0., 1., 0.)
    y = Range(0.01, 1., 1)
    selected_tet = -1
    
    def __init__(self):
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self)
        names, x, y, z = zip(*colors)
        
        self.plot = self.scene.mlab.triangular_mesh(x, y, z, tg.hull,
                                                    color=(1,1,1),
                                                    #opacity=0.3,
                                                    representation='wireframe')
        
        """
        combtet = [[0,1,2],[0,1,3],[0,2,3],[1,2,3]]
        self.plot_selected = self.scene.mlab.triangular_mesh(x, y, z,
                                                             combtet,
                                                             color=(0,.5,1),
                                                             opacity=0.6)
        self.plot_selected.set(visible=False)
        self.plot_point = self.scene.mlab.points3d([self.X], [self.Y], [self.Z])
        self.plot_texts = [self.scene.mlab.text(x=0, y=0, z=0, text="a")
                                          .set(visible=False)
                           for i in range(4)]
        """

    @on_trait_change('scene.activated')
    def create_plot(self):
        self.scene.mlab.axes(extent=[0,100,0,100,0,100])

    @on_trait_change('X,Y,Z')
    def update_XZ(self):
        new_x = self.X/(self.X+self.Y+self.Z)
        new_y = self.Y/(self.X+self.Y+self.Z)
        if abs(self.x-new_x) > 0.001:
            print "x", self.x, new_x
            self.x = new_x
        if abs(self.y-new_y) > 0.001:
            print "y", self.y, new_y
            self.y = new_y

    @on_trait_change('x,y,Y')
    def update_xy(self):
        new_X = (self.Y/self.y)*self.x
        new_Z = (self.Y/self.y)*(1-self.x-self.y)
        if abs(self.X-new_X) > 0.1:
            print "X", self.X, new_X
            self.X = new_X
        if abs(self.Z-new_Z) > 0.1:
            print "Z", self.Z, new_Z
            self.Z = new_Z
    
    @on_trait_change('X,Y,Z')
    def update_plot_selected(self):
        pass
        """
        self.plot_point.mlab_source.set(x=[self.X], y=[self.Y], z=[self.Z])
        point = [self.X,self.Y,self.Z]
        if self.selected_tet != -1:
            verts = [tg.points[i] for i in tg.tets[self.selected_tet]]
            if (geometry.barycentric_coords(verts, point)>=0).all():
                return
        for i, tet in enumerate(tg.tets):
            verts = [tg.points[i] for i in tet]
            if (geometry.barycentric_coords(verts, point)>=0).all():
                self.selected_tet = i
                x, y, z = zip(*[tg.points[i] for i in tet])
                self.plot_selected.mlab_source.set(x=x, y=y, z=z,
                                                   visible=True)

                for i, vert_i in enumerate(tet):
                    text, x, y, z = colors[vert_i]
                    print text, x, y, z
                    self.plot_texts[i].set(x_position=x,
                                           y_position=y,
                                           z_position=z,
                                           text=text,
                                           visible=True)

                return
        self.selected_tet = -1
        self.plot_selected.mlab_source.set(visible=False)
        for plot_text in self.plot_texts:
            plot_text.set(visible=True)
        """ 
        
        
    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                    height=700, width=700, show_label=False),
                HGroup(
                  Item('X', label='X'),
                  Item('Y', label='Y'),
                  Item('Z', label='Z'),
                       ),
                HGroup(
                  Item('x', label='x'),
                  Item('y', label='y'),
                  Item('Y', label='Y'),
                       ),
                )

visualization = Visualization()
visualization.configure_traits()

