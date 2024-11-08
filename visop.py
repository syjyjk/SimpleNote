#coding=utf-8
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

def unify_lons(lons):
  import numpy as np
  return np.array(lons) % 360.

def lons_shift_idxs(lons, lon0):
  idx = ((lons - lon0 ) % 360 ).argsort()
  return idx

def mkdirs(*args):
  import os
  path = os.path.join(*args)
  try:
    os.makedirs(path)
  except OSError:
    pass

def tex_font(font_family="Times New Roman"):
  plt.rcParams.update({"text.usetex":True, "font.family":font_family})

def text_font(font_family="Times New Roman"):
  plt.rc('font', family=font_family)

class myfig(object):
  def __init__(self,figsize_y=1,figsize_x=1,fignum_y=1,fignum_x=1,figscale=6., scheme='1fig1bar',fixed_width=True,fixed_height=False, cbar_orientation='y', y_figsize_scale=np.array([1.]), x_figsize_scale=np.array([1.])):
    import warnings
    import matplotlib.cbook
    #try:
    #  plt.rcParams.update({"text.usetex":True, "font.family":"Times New Roman"})
    #except Exception:
    #  pass
    #  #plt.rcParams.update({"text.usetex":True, "font.family":"Times New Roman"})
    #plt.rc('font', family='Times New Roman')
    warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
    self.figscale = figscale
    self.figsize_x = figscale*1.
    self.figsize_y = figscale*figsize_y/figsize_x
    if fixed_height == True:
      self.figsize_x = figscale*figsize_x/figsize_y
      self.figsize_y = 1.*figscale
    if fixed_width == True:
      self.figsize_x = figscale*1.
      self.figsize_y = figscale*figsize_y/figsize_x
    self.fignum_x  = fignum_x
    self.fignum_y  = fignum_y
    self.xspacescale = 0.2
    self.yspacescale = 0.2
    self.cbarspacescale = 0.05
    self.cbarscale = 0.05
    self.xmarginscale = 0.1
    self.ymarginscale = 0.1
    self.scheme = scheme # '1fig1bar', 'nfig1bar'
    self.cmap = "jet"
    self.cbar_orientation = cbar_orientation
    self.pnscale = 0.1
    self.pnxspacescale = 0.1
    self.pnyspacescale = 0.1
    self.rankorder = "left2right"
    self.y_figsize_scale = np.array(y_figsize_scale)
    self.x_figsize_scale = np.array(x_figsize_scale)
    _ = self.figinit()
    self.n  = 0
    self.ax = None
    self.map= None
    self.nx = 1
    self.ny = 1
    self.lat0 = None
    self.lat1 = None
    self.lon0 = None
    self.lon1 = None
    self.latticks = None
    self.lonticks = None
    self.latticks_fontsize = None
    self.lonticks_fontsize = None
    self.latticks_padding  = None
    self.lonticks_padding  = None

  def set_yfigsize_scale(self, y_figsize_scale):
    self.y_figsize_scale = np.array(y_figsize_scale)
    self.figinit()

  def set_xfigsize_scale(self, x_figsize_scale):
    self.x_figsize_scale = np.array(x_figsize_scale)
    self.figinit()

  def hide_cbar(self):
    self.cbarscale = 0.
    self.cbarspacescale = 0.
    self.figinit()

  def set_xspacescale(self, v):
    self.xspacescale = v
    self.figinit()

  def set_yspacescale(self, v):
    self.yspacescale = v 
    self.figinit()

  def set_cbarspacescale(self, v):
    self.cbarspacescale = v
    self.figinit()

  def set_cbarscale(self, v):
    self.cbarscale = v
    self.figinit()

  def set_xmarginscale(self, v):
    self.xmarginscale = v
    self.figinit()

  def set_ymarginscale(self, v):
    self.ymarginscale = v
    self.figinit()

  def set_cmap(self, v):
    self.cmap = v

  def set_pnscale(self, v):
    self.pnscale = v
    self.figinit()

  def set_pnxspacescale(self, v):
    self.pnxspacescale = v
    self.figinit()

  def set_pnyspacescale(self, v):
    self.pnyspacescale = v
    self.figinit()

  def set_cbar_orientation(self, v):
    self.cbar_orientation = v
    self.figinit()

  def set_rankorder(self, v):
    self.rankorder = v

  def font(self, fontnm):
    plt.rc('font', family=fontnm)

  def figinit(self):
    self.xmarginscalepn = self.xmarginscale + self.pnxspacescale
    self.ymarginscalepn = self.ymarginscale + self.pnyspacescale
    self.y_figsize_arr = np.full((self.fignum_y, self.fignum_x), self.figsize_y) * self.y_figsize_scale[:,np.newaxis]
    self.x_figsize_arr = np.full((self.fignum_y, self.fignum_x), self.figsize_x) * self.x_figsize_scale
    self.y_margin_arr  = np.full((2, self.fignum_x), self.ymarginscalepn*self.figscale)
    self.x_margin_arr  = np.full((self.fignum_y, 2), self.xmarginscalepn*self.figscale)
    self.x_space_arr   = np.full((self.fignum_y , self.fignum_x ), self.xspacescale*self.figscale)
    self.y_space_arr   = np.full((self.fignum_y , self.fignum_x ), self.yspacescale*self.figscale)
    self.x_cbarsize_arr  = np.full((self.fignum_y, self.fignum_x), self.cbarscale*self.figscale)
    self.x_cbarspace_arr = np.full((self.fignum_y, self.fignum_x), self.cbarspacescale*self.figscale)
    self.y_cbarsize_arr  = np.full((self.fignum_y, self.fignum_x), self.cbarscale*self.figscale)
    self.y_cbarspace_arr = np.full((self.fignum_y, self.fignum_x), self.cbarspacescale*self.figscale)
    self.x_space_arr[:,-1] = 0.
    self.y_space_arr[-1,:] = 0.
    if self.scheme == 'nfig1bar': 
      if self.cbar_orientation == 'x':
        self.x_cbarsize_arr[:,:] = 0.
        self.x_cbarspace_arr[:,:] = 0. 
        self.y_cbarsize_arr[:-1,:]  = 0.
        self.y_cbarspace_arr[:-1,:] = 0. 
      elif self.cbar_orientation == 'y':
        self.y_cbarsize_arr[:,:]  = 0.
        self.y_cbarspace_arr[:,:] = 0. 
        self.x_cbarsize_arr[:,:-1]  = 0.
        self.x_cbarspace_arr[:,:-1] = 0. 
    elif self.scheme == '1fig1bar':
      if self.cbar_orientation == 'y':
        self.y_cbarsize_arr[:]  = 0.
        self.y_cbarspace_arr[:] = 0. 
      elif self.cbar_orientation == 'x':
        self.x_cbarsize_arr[:]  = 0.
        self.x_cbarspace_arr[:] = 0. 
    elif self.scheme == 'nfig0bar':
        self.y_cbarsize_arr[:,:]  = 0.
        self.y_cbarspace_arr[:,:] = 0. 
        self.x_cbarsize_arr[:,:]  = 0.
        self.x_cbarspace_arr[:,:] = 0. 
    else:
      raise Exception('self.scheme wrong')

    self.x_totsize =     self.x_figsize_arr[0,:].sum() \
                       + self.x_cbarspace_arr[0,:].sum() \
                       +  self.x_cbarsize_arr[0,:].sum()\
                       +   self.x_space_arr[0,:].sum()\
                       +  self.x_margin_arr[0,:].sum()

    self.y_totsize =     self.y_figsize_arr[:,0].sum() \
                       + self.y_cbarspace_arr[:,0].sum() \
                       +  self.y_cbarsize_arr[:,0].sum()\
                       +   self.y_space_arr[:,0].sum()\
                       +  self.y_margin_arr[:,0].sum()

    self.fig = plt.figure(figsize=[self.x_totsize, self.y_totsize])
    
  def createax(self,ny, nx, barorfig='fig',scale=1., xshiftscale=0., yshiftscale=0.,**kwargs):
    ny_arr = np.array([ny]).flatten()
    nx_arr = np.array([nx]).flatten()
    ny0 = ny_arr[0]
    ny1 = ny_arr[-1]
    nx0 = nx_arr[0]
    nx1 = nx_arr[-1]
    if barorfig == 'fig':
      xposi0 =     self.x_margin_arr[0,0] \
               +  self.x_figsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarspace_arr[0,:nx0-1].sum()\
               + self.x_space_arr[0,:nx0-1].sum()
      xposi1 =      self.x_margin_arr[0,0] \
               +   self.x_figsize_arr[0,:nx1].sum()\
               +    self.x_cbarsize_arr[0,:nx1-1].sum()\
               +   self.x_cbarspace_arr[0,:nx1-1].sum()\
               +     self.x_space_arr[0,:nx1-1].sum()
      yposi1 =   self.y_totsize\
               -    self.y_margin_arr[0   ,   0] \
               -   self.y_figsize_arr[:ny1,  0].sum()\
               -    self.y_cbarsize_arr[:ny1-1,0].sum()\
               -   self.y_cbarspace_arr[:ny1-1,0].sum()\
               -     self.y_space_arr[:ny1-1,0].sum()
      yposi0 =   self.y_totsize\
               -    self.y_margin_arr[0   ,  0] \
               -   self.y_figsize_arr[:ny0-1,0].sum()\
               -    self.y_cbarsize_arr[:ny0-1,0].sum()\
               -   self.y_cbarspace_arr[:ny0-1,0].sum()\
               -     self.y_space_arr[:ny0-1,0].sum()
    if barorfig == 'pn':
      xposi0t =     self.x_margin_arr[0,0] \
               +  self.x_figsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarspace_arr[0,:nx0-1].sum()\
               + self.x_space_arr[0,:nx0-1].sum()
      xposi1t =      self.x_margin_arr[0,0] \
               +   self.x_figsize_arr[0,:nx1].sum()\
               +    self.x_cbarsize_arr[0,:nx1-1].sum()\
               +   self.x_cbarspace_arr[0,:nx1-1].sum()\
               +     self.x_space_arr[0,:nx1-1].sum()
      yposi1t =   self.y_totsize\
               -    self.y_margin_arr[0   ,   0] \
               -   self.y_figsize_arr[:ny1,  0].sum()\
               -    self.y_cbarsize_arr[:ny1-1,0].sum()\
               -   self.y_cbarspace_arr[:ny1-1,0].sum()\
               -     self.y_space_arr[:ny1-1,0].sum()
      yposi0t =   self.y_totsize\
               -    self.y_margin_arr[0   ,  0] \
               -   self.y_figsize_arr[:ny0-1,0].sum()\
               -    self.y_cbarsize_arr[:ny0-1,0].sum()\
               -   self.y_cbarspace_arr[:ny0-1,0].sum()\
               -     self.y_space_arr[:ny0-1,0].sum()

      xposi0  =   xposi0t - self.figscale* self.pnxspacescale - self.figscale * self.pnscale
      xposi1  =   xposi0t - self.figscale* self.pnxspacescale 
      yposi1  =   yposi0t + self.figscale* self.pnyspacescale 
      yposi0  =   yposi0t + self.figscale* self.pnyspacescale + self.figscale * self.pnscale

    if barorfig == 'bar':
      if self.cbar_orientation == 'y':
        xposi0 =     self.x_margin_arr[0,0] \
                 +  self.x_figsize_arr[0,:nx0].sum()\
                 +   self.x_cbarsize_arr[0,:nx0-1].sum()\
                 +   self.x_cbarspace_arr[0,:nx0].sum()\
                 + self.x_space_arr[0,:nx0-1].sum()
        xposi1 =      self.x_margin_arr[0,0] \
                 +   self.x_figsize_arr[0,:nx1].sum()\
                 +    self.x_cbarsize_arr[0,:nx1].sum()\
                 +   self.x_cbarspace_arr[0,:nx1].sum()\
                 +     self.x_space_arr[0,:nx1-1].sum()
        yposi1 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,   0] \
                 -   self.y_figsize_arr[:ny1,  0].sum()\
                 -    self.y_cbarsize_arr[:ny1-1,0].sum()\
                 -   self.y_cbarspace_arr[:ny1-1,0].sum()\
                 -     self.y_space_arr[:ny1-1,0].sum()
        yposi0 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,  0] \
                 -   self.y_figsize_arr[:ny0-1,0].sum()\
                 -    self.y_cbarsize_arr[:ny0-1,0].sum()\
                 -   self.y_cbarspace_arr[:ny0-1,0].sum()\
                 -     self.y_space_arr[:ny0-1,0].sum()
      if self.cbar_orientation == 'x':
        xposi0 =     self.x_margin_arr[0,0] \
                 +  self.x_figsize_arr[0,:nx0-1].sum()\
                 +   self.x_cbarsize_arr[0,:nx0-1].sum()\
                 +   self.x_cbarspace_arr[0,:nx0-1].sum()\
                 + self.x_space_arr[0,:nx0-1].sum()
        xposi1 =      self.x_margin_arr[0,0] \
                 +   self.x_figsize_arr[0,:nx1].sum()\
                 +    self.x_cbarsize_arr[0,:nx1-1].sum()\
                 +   self.x_cbarspace_arr[0,:nx1-1].sum()\
                 +     self.x_space_arr[0,:nx1-1].sum()
        yposi1 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,   0] \
                 -   self.y_figsize_arr[:ny1,  0].sum()\
                 -    self.y_cbarsize_arr[:ny1,0].sum()\
                 -   self.y_cbarspace_arr[:ny1,0].sum()\
                 -     self.y_space_arr[:ny1-1,0].sum()
        yposi0 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,  0] \
                 -   self.y_figsize_arr[:ny0,0].sum()\
                 -    self.y_cbarsize_arr[:ny0-1,0].sum()\
                 -   self.y_cbarspace_arr[:ny0,0].sum()\
                 -     self.y_space_arr[:ny0-1,0].sum()
    sx0 = xposi0/ self.x_totsize
    sy0 = yposi1/ self.y_totsize
    ssx = (xposi1 - xposi0)/ self.x_totsize
    ssy = (yposi0 - yposi1) / self.y_totsize

    ax =self.fig.add_axes([sx0-ssx*((1.-scale)/2.+xshiftscale), sy0+ssy*((1.-scale)/2.+yshiftscale), ssx*scale, ssy*scale],**kwargs)
    self.ax = ax
    self.nx = nx1
    self.ny = ny1
    if barorfig == "pn":
      self.nx = 1
      self.ny = 1
      self.n = 0
    else:
      self.n  = (ny1 - 1)*self.fignum_x + nx1
    self.set_title_fontsize(20)
    self.set_xticks_fontsize(15)
    self.set_yticks_fontsize(15)
    self.set_xlabel_fontsize(15)
    self.set_ylabel_fontsize(15)
    #self.set_xlabel_padding(40)
    #self.set_ylabel_padding(20)

    self.map = None
    self.lat0 = -90.
    self.lat1 =  90.
    self.lon0 =  0
    self.lon1 =  360
    self.latticks = [-60, 0, 60]
    self.lonticks =[0, 60, 120, 180, 240, 300 ]
    self.latticks_fontsize = 15
    self.lonticks_fontsize = 15
    self.latticks_padding  = 1.5
    self.lonticks_padding  = 1.5
    return self.ax

  def new_ax(self, n1=None, n2=None,barorfig='fig', scale=1, xshiftscale=0., yshiftscale=0., **kwargs):
    if n2 != None and n1 !=None:
      return self.createax(n1, n2, barorfig=barorfig, scale=scale, xshiftscale=xshiftscale, yshiftscale=yshiftscale, **kwargs)
    elif n2 == None:
      return self.ncreate(n1, barorfig=barorfig, scale=scale, xshiftscale=xshiftscale, yshiftscale=yshiftscale, **kwargs)

  #def newax(self, n1=None, n2=None, barorfig='fig', scale=1., xshiftscale=0., yshiftscale=0.,**kwargs):
  #  if n2 != None and n1 !=None:
  #    return self.createax(n1, n2, barorfig=barorfig, scale=scale, xshiftscale=xshiftscale, yshiftscale=yshiftscale, **kwargs)
  #  elif n2 == None:
  #    return self.ncreate(n1, barorfig=barorfig, scale=scale, xshiftscale=xshiftscale, yshiftscale=yshiftscale, **kwargs)

  def newax(self,n=None,barorfig='fig',scale=1., xshiftscale=0., yshiftscale=0., **kwargs):
    order = self.rankorder
    if n == None:
      n = self.n + 1
      self.n = n
    else:
      self.n = n
    #order -> 'up2down', 'left2right'
    if order == 'left2right':
      nx = ((n -1) % self.fignum_x) + 1
      ny = ((n -1) // self.fignum_x) + 1
    elif order == 'up2down':
      nx = ((n-1) // self.fignum_y) + 1
      ny = ((n-1) % self.fignum_y) + 1
    else:
      raise Exception('ncreate-> order wrong')
    return self.createax(ny,nx,barorfig,scale=scale, xshiftscale=xshiftscale, yshiftscale=yshiftscale, **kwargs)


  
  def create(self, n1=None, n2=None,barorfig='fig', scale=1., xshiftscale=0., yshiftscale=0.,**kwargs):
    if n2 != None and n1 !=None:
      return self.createax(n1, n2, barorfig=barorfig, scale=scale,xshiftscale=xshiftscale, yshiftscale=yshiftscale,**kwargs)
    elif n2 == None:
      return self.ncreate(n1, barorfig=barorfig, scale=scale, xshiftscale=xshiftscale, yshiftscale=yshiftscale,**kwargs)

  def twinax(self, color=None, twinx=True):
    self.tempax = self.fig.add_axes(self.ax.get_position())
    self.tempax.patch.set_visible(False)
    self.tempax.yaxis.set_label_position('right')
    self.tempax.xaxis.set_label_position('top')
    self.tempax.yaxis.set_ticks_position('right')
    self.tempax.xaxis.set_ticks_position('top')
    self.tempax.tick_params(axis="x", labelsize=15)
    self.tempax.tick_params(axis="y", labelsize=15)
    self.tempax.set_xlim(self.ax.get_xlim())
    self.ax = self.tempax
    return self.ax


  def ncreate(self,n=None,barorfig='fig',scale=1., xshiftscale=0., yshiftscale=0., **kwargs):
    order = self.rankorder
    if n == None:
      n = self.n + 1
      self.n = n
    else:
      self.n = n
    #order -> 'up2down', 'left2right'
    if order == 'left2right':
      nx = ((n -1) % self.fignum_x) + 1
      ny = ((n -1) // self.fignum_x) + 1
    elif order == 'up2down':
      nx = ((n-1) // self.fignum_y) + 1
      ny = ((n-1) % self.fignum_y) + 1
    else:
      raise Exception('ncreate-> order wrong')
    return self.createax(ny,nx,barorfig,scale=scale, xshiftscale=xshiftscale, yshiftscale=yshiftscale, **kwargs)

  def add_cbar(self,cbar,ax=None,ticks=None,tickvalues=None,**kwargs):
    nx = self.nx 
    ny = self.ny
    # set current cbar
    if self.cbar_orientation == 'x':
      orientation = 'horizontal'
    else:
      orientation = 'vertical'

    if ax == None:
      self.cbarax = self.createax(ny,nx,'bar')
    else:
      self.cbarax = ax
    self.ax = self.cbarax
    if type(ticks) == type(None):
      vmin, vmax = cbar.get_clim()
      ticks = np.linspace(vmin,vmax,10)
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
        print('#####',tickvalues)
    else: 
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
    return temp.ax
    

  def ccbar(self,cbar,ax=None,ticks=None,tickvalues=None,**kwargs):
    nx = self.nx 
    ny = self.ny
    # set current cbar
    if self.cbar_orientation == 'x':
      orientation = 'horizontal'
    else:
      orientation = 'vertical'

    if ax == None:
      self.cbarax = self.createax(ny,nx,'bar')
    else:
      self.cbarax = ax
    self.ax = self.cbarax
    if type(ticks) == type(None):
      vmin, vmax = cbar.get_clim()
      ticks = np.linspace(vmin,vmax,10)
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
        print('#####',tickvalues)
    else: 
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
    return temp.ax
    
  def colorbar(self,ny,nx,cbar,ax=None,ticks=None,tickvalues=None,**kwargs):
    if self.cbar_orientation == 'x':
      orientation = 'horizontal'
    else:
      orientation = 'vertical'

    if ax == None:
      self.cbarax = self.createax(ny,nx,'bar')
    else:
      self.cbarax = ax

    if type(ticks) == type(None):
      vmin, vmax = cbar.get_clim()
      ticks = np.linspace(vmin,vmax,10)
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
        print('#####',tickvalues)
    else: 
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
    return temp.ax

  def pn(self, n, content=None, fontsize=20, prefixstr=r"({})", **kwargs):
    if content == None:
      alphabet='abcdefghijklmnopqrstuvwxyz'
      if n > 24:
        aln = str(n)
      else:
        aln     = alphabet[n-1]
      prefix = prefixstr.format(aln)
    else:
      prefix = content
    ax = self.ncreate(n, 'pn')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.ylim([0,1])
    plt.xlim([0,1])
    plt.axis('off')
    plt.text(0,0, prefix, fontsize=fontsize, **kwargs)
    return ax

  def new_legend(self, *args, fontsize=15, **kwargs):
    return self.ax.legend(*args, fontsize=15, **kwargs)

  def add_legend(self, *args, fontsize=15, **kwargs):
    return self.ax.legend(*args, fontsize=15, **kwargs)

  def legend(self, *args, fontsize=15, **kwargs):
    return self.ax.legend(*args, fontsize=15, **kwargs)

  def set_title(self, title='', fontdict=None, loc='center', pad=None, fontsize=20, **kwargs):
    plt.title( title, fontdict=fontdict, loc=loc, pad=pad, fontsize=fontsize, **kwargs)

  def get_title(self):
    return self.ax.get_title()
  
  def preset_latlim(self, lat0=None, lat1=None):
    if lat0==None and lat1==None:
      self.lat0 = -90
      self.lat1 = 90
    elif lat1==None and lat0!=None:
      self.lat0 = lat0[0]
      self.lat1 = lat0[1]
    elif lat1!=None and lat0!=None:
      self.lat0 = lat0
      self.lat1 = lat1

  def preset_lonlim(self, lon0=None, lon1=None):
    if lon0==None and lon1==None:
      self.lon0 = 0
      self.lon1 = 360
    elif lon1==None and lon0!=None:
      self.lon0 = lon0[0]
      self.lon1 = lon0[1]
    elif lon1!=None and lon0!=None:
      self.lon0 = lon0
      self.lon1 = lon1 

  def preset_latticks_padding(self,v):
    self.latticks_padding = v

  def preset_lonticks_padding(self,v):
    self.lonticks_padding = v

  def preset_lonticks(self, v, intv=None):
    self.lonticks = v
    if intv != None:
      self.lonticks = np.arange(0,359.,intv)

  def preset_latticks(self, v,intv=None):
    self.latticks = v
    if intv != None:
      self.latticks = np.append(np.arange(0,-91, -intv), np.arange(intv, 91, intv))

  def preset_latticks_fontsize(self,v):
    self.latticks_fontsize = v

  def preset_lonticks_fontsize(self,v):
    self.lonticks_fontsize = v
  
  def set_title_padding(self, pad):
    self.ax._set_title_offset_trans(float(pad))

  def set_title_fontsize(self, fontsize):
    self.ax.title.set_size(fontsize)

  def set_figtitle(self, title, fontsize=25,**kwargs):
    self.fig.suptitle( title, fontsize=fontsize,**kwargs )

  def figtitle(self, title, fontsize=25,**kwargs):
    self.fig.suptitle( title, fontsize=fontsize,**kwargs )



  def get_ylim(self):
    return self.ax.get_ylim()

  def get_xlim(self):
    return self.ax.get_xlim()
  
  def get_xticks(self):
    return self.ax.get_xticks()

  def get_yticks(self):
    return self.ax.get_yticks()

  def get_xlabel(self):
    return self.ax.xaxis.get_label()

  def get_ylabel(self):
    return self.ax.yaxis.get_label()

  def set_xlabel(self, label, *arg, **kwargs):
    self.ax.set_xlabel(label, fontsize=15, *arg, **kwargs)

  def set_ylabel(self, label, *arg, **kwargs):
    self.ax.set_ylabel(label, fontsize=15, *arg, **kwargs)

  def set_xticks(self, ticks, ticklabels=None, *arg, **kwargs):
    import matplotlib.pyplot as plt
    if ticklabels == None:
      self.ax.set_xticks(ticks, ticklabels=ticklabels, *arg, **kwargs)
    else:
      plt.xticks(ticks, ticklabels, *arg, **kwargs)

  def set_xticks_color(self, color=None):
    if color != None:
      self.ax.tick_params(axis="x", colors=color)

  def set_yticks_color(self, color=None):
    if color != None:
      self.ax.tick_params(axis="y", colors=color)

  def set_xlabel_color(self, color):
    if color != None:
      self.ax.xaxis.label.set_color(color)

  def set_ylabel_color(self, color):
    if color != None:
      self.ax.yaxis.label.set_color(color)

  def set_yticks(self, ticks, ticklabels=None, *arg, **kwargs):
    import matplotlib.pyplot as plt
    if ticklabels == None:
      self.ax.set_yticks(ticks, ticklabels=ticklabels, *arg, **kwargs)
    else:
      plt.yticks(ticks, ticklabels, *arg, **kwargs)

  def set_xlim(self, *args, **kwargs):
    if not args and not kwargs:
      pass
    else:
      ret = self.ax.set_xlim(*args, **kwargs)

  def set_ylim(self, *args, **kwargs):
    if not args and not kwargs:
      pass
    else:
      ret = self.ax.set_ylim(*args, **kwargs)

  def set_xlabel_fontsize(self, fontsize):
    self.ax.xaxis.get_label().set_fontsize(fontsize)

  def set_ylabel_fontsize(self, fontsize):
    self.ax.yaxis.get_label().set_fontsize(fontsize)

  def set_xlabel_padding(self, pad):
    self.ax.xaxis.labelpad = pad

  def set_ylabel_padding(self, pad):
    self.ax.yaxis.labelpad = pad

  def set_xticks_fontsize(self, fontsize):
    for xtick in self.ax.xaxis.get_major_ticks():
      xtick.label.set_fontsize(fontsize)

  def set_xticks_padding(self, pad):
    for xtick in self.ax.xaxis.get_major_ticks():
      xtick.set_pad(pad)

  def set_yticks_padding(self, pad):
    for ytick in self.ax.yaxis.get_major_ticks():
      ytick.set_pad(pad)

  def set_yticks_fontsize(self, fontsize):
    for xtick in self.ax.yaxis.get_major_ticks():
      xtick.label.set_fontsize(fontsize)
 

  def show(self):
    plt.show()

  def savefig(self, fname, dpi=None, facecolor='white', edgecolor='white', bbox_inches='tight', **kwargs ):
    import os
    dirname = os.path.dirname(fname)
    mkdirs(dirname)
    plt.savefig(fname,dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, bbox_inches=bbox_inches ,**kwargs)
  
  
  #def savefig2(self, fname, dpi=None, facecolor='white', edgecolor='white', bbox_inches='tight',
  #             base= os.path.join(os.environ['HOME'], "Database",'Projects'), 
  #             path2=os.path.join(os.environ['HOME'], 'SynologyDrive', 'Projects'),
  #             **kwargs ):
  #  import os
  #  thecwd = os.getcwd()
  #  base   = base
  #  relcwd = os.path.relpath(thecwd, base)
  #  if relcwd == '.':
  #    relcwd == ''
  #  path2 = path2
  #  final_path = os.path.join(path2,relcwd,fname)
  #  dirname = os.path.dirname(final_path)
  #  mkdirs(dirname)
  #  plt.savefig(final_path,dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, bbox_inches=bbox_inches ,**kwargs)

  def addmapax(self,lat0=None,lat1=None,
             lon0=None,lon1=None,
             show_coastline=True,
             show_dashes=False,
             **kwargs):
    if lat0 != None:
      self.lat0 = lat0
    if lat1 != None:
      self.lat1 = lat1
    if lon0 != None:
      self.lon0 = lon0
    if lon1 != None:
      self.lon1 = lon1

    from mpl_toolkits.basemap import Basemap
    self.newax()
    map0 = Basemap(resolution='c',area_thresh=1000,
                   llcrnrlat=float(self.lat0),llcrnrlon=float(self.lon0),
                   urcrnrlat=float(self.lat1),urcrnrlon=float(self.lon1),
                   ax=self.ax, **kwargs)
    if show_coastline:
      map0.drawcoastlines()
    if show_dashes != True:
      dashes = [1,1000000]
    else:
      dashes = [5,8]
    map0.drawparallels(self.latticks,labels=[True,False,False,False],dashes=dashes,fontsize=self.latticks_fontsize,xoffset=self.latticks_padding)
    map0.drawmeridians(self.lonticks,labels=[False,False,False,True],dashes=dashes,fontsize=self.lonticks_fontsize,yoffset=self.lonticks_padding)
    self.map = map0

  def addmap(self,lat0=None,lat1=None,
             lon0=None,lon1=None,
             show_coastline=True,
             show_dashes=False,
             **kwargs):
    if lat0 != None:
      self.lat0 = lat0
    if lat1 != None:
      self.lat1 = lat1
    if lon0 != None:
      self.lon0 = lon0
    if lon1 != None:
      self.lon1 = lon1

    from mpl_toolkits.basemap import Basemap
    map0 = Basemap(resolution='c',area_thresh=1000,
                   llcrnrlat=float(self.lat0),llcrnrlon=float(self.lon0),
                   urcrnrlat=float(self.lat1),urcrnrlon=float(self.lon1),
                   ax=self.ax, **kwargs)
    if show_coastline:
      map0.drawcoastlines()
    if show_dashes != True:
      dashes = [1,1000000]
    else:
      dashes = [5,8]
    map0.drawparallels(self.latticks,labels=[True,False,False,False],dashes=dashes,fontsize=self.latticks_fontsize,xoffset=self.latticks_padding)
    map0.drawmeridians(self.lonticks,labels=[False,False,False,True],dashes=dashes,fontsize=self.lonticks_fontsize,yoffset=self.lonticks_padding)
    self.map = map0

  def add_map(self,lat0=None,lat1=None,
             lon0=None,lon1=None,
             show_coastline=True,
             show_dashes=False,
             **kwargs):
    if lat0 != None:
      self.lat0 = lat0
    if lat1 != None:
      self.lat1 = lat1
    if lon0 != None:
      self.lon0 = lon0
    if lon1 != None:
      self.lon1 = lon1

    from mpl_toolkits.basemap import Basemap
    map0 = Basemap(resolution='c',area_thresh=1000,
                   llcrnrlat=float(self.lat0),llcrnrlon=float(self.lon0),
                   urcrnrlat=float(self.lat1),urcrnrlon=float(self.lon1),
                   ax=self.ax, **kwargs)
    if show_coastline:
      map0.drawcoastlines()
    if show_dashes != True:
      dashes = [1,1000000]
    else:
      dashes = [5,8]
    map0.drawparallels(self.latticks,labels=[True,False,False,False],dashes=dashes,fontsize=self.latticks_fontsize,xoffset=self.latticks_padding)
    map0.drawmeridians(self.lonticks,labels=[False,False,False,True],dashes=dashes,fontsize=self.lonticks_fontsize,yoffset=self.lonticks_padding)
    self.map = map0
   
  def map_imshow(self, lats, lons, arr,**kwargs):
    lons_idxs = lons_shift_idxs(unify_lons(lons), self.lon0%360 )
    lons = unify_lons(lons[lons_idxs] - self.lon0) + self.lon0

    newarr = np.array(arr[:, lons_idxs])
    if lats.shape != newarr.shape and lons.shape!= newarr.shape:
      llons, llats = np.meshgrid(lons, lats)
    else:
      llons, llats = lons, lats
    if self.map != None:
      llons, llats = self.map(llons, llats)
    cbar = self.ax.pcolormesh(llons, llats, newarr, **kwargs)
    return cbar

  def imshow(self, arr,**kwargs):
    nx, ny = arr.shape
    lats   = np.arange(nx)
    lons   = np.arange(ny)
    newarr = np.array(arr)
    cbar = self.ax.pcolormesh(lons, lats, newarr, **kwargs)
    return cbar

  def map_plot(self, lats, lons, *args,**kwargs):
    xs, ys = self.map(lons, lats)
    self.ax.plot(xs, ys, *args, **kwargs)

  def shade(self, x, y, where=None, ylims=None, color=None):
    if ylims == None:
      ylims = self.get_ylim()
    self.ax.fill_between(x, y, y2=ylims[0], where=where, color=color)
    plt.ylim(*ylims)








































'''
### Usage Demo ####
mf = multifig(figsize_y,figsize_x,fignum_y,fignum_x,figscale=1.,scheme='1fig1bar') # fixed_width=None,fixed_height=None 可选
########## 参数说明 ####################################################
# figsize_y -> 子图的纵向尺寸
# figsize_x -> 子图的横向尺寸
# *** (默认) 将子图的横向宽度设定为 单位长度。因而纵向长度为 figsize_y / figsize_x
# *** 这样一来 子图的长宽比例固定，且方便多图排版。
# *** 如果尺寸不合适， 可通过 figscale 进行放大或缩小
# *** 如果想改用纵向高度为 单位长度, 可令 fixed_height=True
# fignum_y  -> 纵向排列 fignum_y 张子图
# fignum_x  -> 横向排列 fignum_x 张子图
# scheme    -> 三种模式可供选择 '1fig1bar', 'nfig1bar', 'nfig0bar'
########################################################################
########## 初始化设置 ##################################################
# 如果不进行初始化设置,会选用默认初始化方案。 
# 如果需要自定以初始化设置，各参数设定完成后, 只有通过 mf.figinit() 才能领新初始化方案生效。
mf.xmarginscale   = r1 #  r1>0 , r1 的值最好不要大于 1. 否则图可能不美观 
mf.ymarginscale   = r2 #  r2>0 , r2 的值最好不要大于 1. 否则图可能不美观
mf.xspacescale    = r3 #  r3>0 , r3 的值最好不要大于 1. 否则图可能不美观
mf.yspacescale    = r4 #  r4>0 , r4 的值最好不要大于 1. 否则图可能不美观
mf.cbarspacescale = r5 #  r5>0 , r5 的值最好不要大于 1. 否则图可能不美观
mf.cbarscale      = r6 #  r6>0 , r6 的值最好不要大于 1. 否则图可能不美观
mf.cbar_orientation = # 'y', 'x'
mf.scheme         = # 1fig1bar # nfig1bar # nfig0bar
mf.figinit()         
########## 初始化设置结束 ##############################################
# P.S.  mf.fig --> fig
figax  = mf.create(ny0,nx0)         # ny0 <= fignum_y , nx0 <= fignum_x;
figax  = mf.ncreate(nt,barorfig='fig',order='left2right')
cbarax = mf.create(ny1,nx1, 'bar')
# mf.colorbar(ny,nx,cbar,ax=None,ticks=None,tickvalues=None,**kwargs) --> Editing Now!!
'''

class multifig(object):
  def __init__(self,figsize_y,figsize_x,fignum_y,fignum_x,figscale=4.,scheme='1fig1bar',fixed_width=True,fixed_height=False, cbar_orientation='y'):
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
    self.figscale = figscale
    self.figsize_x = figscale*1.
    self.figsize_y = figscale*figsize_y/figsize_x
    if fixed_height == True:
      self.figsize_x = figscale*figsize_x/figsize_y
      self.figsize_y = 1.*figscale
    if fixed_width == True:
      self.figsize_x = figscale*1.
      self.figsize_y = figscale*figsize_y/figsize_x
    self.fignum_x  = fignum_x
    self.fignum_y  = fignum_y
    self.xspacescale = 0.1
    self.yspacescale = 0.1
    self.cbarspacescale = 0.1
    self.cbarscale = 0.1
    self.xmarginscale = 0.1
    self.ymarginscale = 0.1
    self.scheme = scheme # '1fig1bar', 'nfig1bar'
    self.cbar_orientation = cbar_orientation
    self.pnscale = 0.1
    self.pnxspacescale = 0.1
    self.pnyspacescale = 0.1
    self.ax = None
    self.nx = None
    self.ny = None
    _ = self.figinit()

  def font(self, fontnm):
    plt.rc('font', family=fontnm)

  def figinit(self):
    self.xmarginscalepn = self.xmarginscale + self.pnxspacescale
    self.ymarginscalepn = self.ymarginscale + self.pnyspacescale
    self.y_figsize_arr = np.full((self.fignum_y, self.fignum_x), self.figsize_y)
    self.x_figsize_arr = np.full((self.fignum_y, self.fignum_x), self.figsize_x)
    self.y_margin_arr  = np.full((2, self.fignum_x), self.ymarginscalepn*self.figscale)
    self.x_margin_arr  = np.full((self.fignum_y, 2), self.xmarginscalepn*self.figscale)
    self.x_space_arr   = np.full((self.fignum_y , self.fignum_x ), self.xspacescale*self.figscale)
    self.y_space_arr   = np.full((self.fignum_y , self.fignum_x ), self.yspacescale*self.figscale)
    self.x_cbarsize_arr  = np.full((self.fignum_y, self.fignum_x), self.cbarscale*self.figscale)
    self.x_cbarspace_arr = np.full((self.fignum_y, self.fignum_x), self.cbarspacescale*self.figscale)
    self.y_cbarsize_arr  = np.full((self.fignum_y, self.fignum_x), self.cbarscale*self.figscale)
    self.y_cbarspace_arr = np.full((self.fignum_y, self.fignum_x), self.cbarspacescale*self.figscale)
    self.x_space_arr[:,-1] = 0.
    self.y_space_arr[-1,:] = 0.
    if self.scheme == 'nfig1bar': 
      if self.cbar_orientation == 'x':
        self.x_cbarsize_arr[:,:] = 0.
        self.x_cbarspace_arr[:,:] = 0. 
        self.y_cbarsize_arr[:-1,:]  = 0.
        self.y_cbarspace_arr[:-1,:] = 0. 
      elif self.cbar_orientation == 'y':
        self.y_cbarsize_arr[:,:]  = 0.
        self.y_cbarspace_arr[:,:] = 0. 
        self.x_cbarsize_arr[:,:-1]  = 0.
        self.x_cbarspace_arr[:,:-1] = 0. 
    elif self.scheme == '1fig1bar':
      if self.cbar_orientation == 'y':
        self.y_cbarsize_arr[:]  = 0.
        self.y_cbarspace_arr[:] = 0. 
      elif self.cbar_orientation == 'x':
        self.x_cbarsize_arr[:]  = 0.
        self.x_cbarspace_arr[:] = 0. 
    elif self.scheme == 'nfig0bar':
        self.y_cbarsize_arr[:,:]  = 0.
        self.y_cbarspace_arr[:,:] = 0. 
        self.x_cbarsize_arr[:,:]  = 0.
        self.x_cbarspace_arr[:,:] = 0. 
    else:
      raise Exception('self.scheme wrong')

    self.x_totsize =     self.x_figsize_arr[0,:].sum() \
                       + self.x_cbarspace_arr[0,:].sum() \
                       +  self.x_cbarsize_arr[0,:].sum()\
                       +   self.x_space_arr[0,:].sum()\
                       +  self.x_margin_arr[0,:].sum()

    self.y_totsize =     self.y_figsize_arr[:,0].sum() \
                       + self.y_cbarspace_arr[:,0].sum() \
                       +  self.y_cbarsize_arr[:,0].sum()\
                       +   self.y_space_arr[:,0].sum()\
                       +  self.y_margin_arr[:,0].sum()

    self.fig = plt.figure(figsize=[self.x_totsize, self.y_totsize])
    
  def create(self,ny,nx,barorfig='fig',**kwargs):
    ny_arr = np.array([ny]).flatten()
    nx_arr = np.array([nx]).flatten()
    ny0 = ny_arr[0]
    ny1 = ny_arr[-1]
    nx0 = nx_arr[0]
    nx1 = nx_arr[-1]
    if barorfig == 'fig':
      xposi0 =     self.x_margin_arr[0,0] \
               +  self.x_figsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarspace_arr[0,:nx0-1].sum()\
               + self.x_space_arr[0,:nx0-1].sum()
      xposi1 =      self.x_margin_arr[0,0] \
               +   self.x_figsize_arr[0,:nx1].sum()\
               +    self.x_cbarsize_arr[0,:nx1-1].sum()\
               +   self.x_cbarspace_arr[0,:nx1-1].sum()\
               +     self.x_space_arr[0,:nx1-1].sum()
      yposi1 =   self.y_totsize\
               -    self.y_margin_arr[0   ,   0] \
               -   self.y_figsize_arr[:ny1,  0].sum()\
               -    self.y_cbarsize_arr[:ny1-1,0].sum()\
               -   self.y_cbarspace_arr[:ny1-1,0].sum()\
               -     self.y_space_arr[:ny1-1,0].sum()
      yposi0 =   self.y_totsize\
               -    self.y_margin_arr[0   ,  0] \
               -   self.y_figsize_arr[:ny0-1,0].sum()\
               -    self.y_cbarsize_arr[:ny0-1,0].sum()\
               -   self.y_cbarspace_arr[:ny0-1,0].sum()\
               -     self.y_space_arr[:ny0-1,0].sum()
    if barorfig == 'pn':
      xposi0t =     self.x_margin_arr[0,0] \
               +  self.x_figsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarsize_arr[0,:nx0-1].sum()\
               +   self.x_cbarspace_arr[0,:nx0-1].sum()\
               + self.x_space_arr[0,:nx0-1].sum()
      xposi1t =      self.x_margin_arr[0,0] \
               +   self.x_figsize_arr[0,:nx1].sum()\
               +    self.x_cbarsize_arr[0,:nx1-1].sum()\
               +   self.x_cbarspace_arr[0,:nx1-1].sum()\
               +     self.x_space_arr[0,:nx1-1].sum()
      yposi1t =   self.y_totsize\
               -    self.y_margin_arr[0   ,   0] \
               -   self.y_figsize_arr[:ny1,  0].sum()\
               -    self.y_cbarsize_arr[:ny1-1,0].sum()\
               -   self.y_cbarspace_arr[:ny1-1,0].sum()\
               -     self.y_space_arr[:ny1-1,0].sum()
      yposi0t =   self.y_totsize\
               -    self.y_margin_arr[0   ,  0] \
               -   self.y_figsize_arr[:ny0-1,0].sum()\
               -    self.y_cbarsize_arr[:ny0-1,0].sum()\
               -   self.y_cbarspace_arr[:ny0-1,0].sum()\
               -     self.y_space_arr[:ny0-1,0].sum()

      xposi0  =   xposi0t - self.figscale* self.pnxspacescale - self.figscale * self.pnscale
      xposi1  =   xposi0t - self.figscale* self.pnxspacescale 
      yposi1  =   yposi0t + self.figscale* self.pnyspacescale 
      yposi0  =   yposi0t + self.figscale* self.pnyspacescale + self.figscale * self.pnscale

    if barorfig == 'bar':
      if self.cbar_orientation == 'y':
        xposi0 =     self.x_margin_arr[0,0] \
                 +  self.x_figsize_arr[0,:nx0].sum()\
                 +   self.x_cbarsize_arr[0,:nx0-1].sum()\
                 +   self.x_cbarspace_arr[0,:nx0].sum()\
                 + self.x_space_arr[0,:nx0-1].sum()
        xposi1 =      self.x_margin_arr[0,0] \
                 +   self.x_figsize_arr[0,:nx1].sum()\
                 +    self.x_cbarsize_arr[0,:nx1].sum()\
                 +   self.x_cbarspace_arr[0,:nx1].sum()\
                 +     self.x_space_arr[0,:nx1-1].sum()
        yposi1 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,   0] \
                 -   self.y_figsize_arr[:ny1,  0].sum()\
                 -    self.y_cbarsize_arr[:ny1-1,0].sum()\
                 -   self.y_cbarspace_arr[:ny1-1,0].sum()\
                 -     self.y_space_arr[:ny1-1,0].sum()
        yposi0 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,  0] \
                 -   self.y_figsize_arr[:ny0-1,0].sum()\
                 -    self.y_cbarsize_arr[:ny0-1,0].sum()\
                 -   self.y_cbarspace_arr[:ny0-1,0].sum()\
                 -     self.y_space_arr[:ny0-1,0].sum()
      if self.cbar_orientation == 'x':
        xposi0 =     self.x_margin_arr[0,0] \
                 +  self.x_figsize_arr[0,:nx0-1].sum()\
                 +   self.x_cbarsize_arr[0,:nx0-1].sum()\
                 +   self.x_cbarspace_arr[0,:nx0-1].sum()\
                 + self.x_space_arr[0,:nx0-1].sum()
        xposi1 =      self.x_margin_arr[0,0] \
                 +   self.x_figsize_arr[0,:nx1].sum()\
                 +    self.x_cbarsize_arr[0,:nx1-1].sum()\
                 +   self.x_cbarspace_arr[0,:nx1-1].sum()\
                 +     self.x_space_arr[0,:nx1-1].sum()
        yposi1 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,   0] \
                 -   self.y_figsize_arr[:ny1,  0].sum()\
                 -    self.y_cbarsize_arr[:ny1,0].sum()\
                 -   self.y_cbarspace_arr[:ny1,0].sum()\
                 -     self.y_space_arr[:ny1-1,0].sum()
        yposi0 =   self.y_totsize\
                 -    self.y_margin_arr[0   ,  0] \
                 -   self.y_figsize_arr[:ny0,0].sum()\
                 -    self.y_cbarsize_arr[:ny0-1,0].sum()\
                 -   self.y_cbarspace_arr[:ny0,0].sum()\
                 -     self.y_space_arr[:ny0-1,0].sum()
    sx0 = xposi0/ self.x_totsize
    sy0 = yposi1/ self.y_totsize
    ssx = (xposi1 - xposi0)/ self.x_totsize
    ssy = (yposi0 - yposi1) / self.y_totsize
    ax =self.fig.add_axes([sx0, sy0, ssx, ssy],**kwargs)
    self.ax = ax
    self.nx = nx
    self.ny = ny
    return ax

  

  def ncreate(self,n,barorfig='fig',order='left2right',**kwargs):
    self.n = n
    #order -> 'up2down', 'left2right'
    if order == 'left2right':
      nx = ((n -1) % self.fignum_x) + 1
      ny = ((n -1) // self.fignum_x) + 1
    elif order == 'up2down':
      nx = ((n-1) // self.fignum_y) + 1
      ny = ((n-1) % self.fignum_y) + 1
    else:
      raise Exception('ncreate-> order wrong')
    return self.create(ny,nx,barorfig,**kwargs)

  def ccbar(self,cbar,ax=None,ticks=None,tickvalues=None,**kwargs):
    nx = self.nx 
    ny = self.ny
    # set current cbar
    if self.cbar_orientation == 'x':
      orientation = 'horizontal'
    else:
      orientation = 'vertical'

    if ax == None:
      self.cbarax = self.create(ny,nx,'bar')
    else:
      self.cbarax = ax
    self.ax = self.cbarax
    if type(ticks) == type(None):
      vmin, vmax = cbar.get_clim()
      ticks = np.linspace(vmin,vmax,10)
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
        print('#####',tickvalues)
    else: 
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
    return temp.ax
    
  def colorbar(self,ny,nx,cbar,ax=None,ticks=None,tickvalues=None,**kwargs):
    if self.cbar_orientation == 'x':
      orientation = 'horizontal'
    else:
      orientation = 'vertical'

    if ax == None:
      self.cbarax = self.create(ny,nx,'bar')
    else:
      self.cbarax = ax

    if type(ticks) == type(None):
      vmin, vmax = cbar.get_clim()
      ticks = np.linspace(vmin,vmax,10)
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
        print('#####',tickvalues)
    else: 
      temp = self.fig.colorbar(cbar,self.cbarax,ticks=ticks,orientation=orientation,**kwargs)
      if type(tickvalues) != type(None):
        if self.cbar_orientation == 'x':
          temp.ax.set_xticks(ticks)
          temp.ax.set_xticklabels(tickvalues)
        else:
          temp.ax.set_yticks(ticks)
          temp.ax.set_yticklabels(tickvalues)
    return temp.ax

  def pn(self, n ,content=None, fontsize=20):
    if content == None:
      
      alphabet='abcdefghijklmnopqrstuvwxyz'
      if n > 24:
        aln = str(n)
      else:
        aln     = alphabet[n-1]
      prefix = '({})'.format(aln)
    else:
      prefix = content

    ax = self.ncreate(n, 'pn')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.ylim([0,1])
    plt.xlim([0,1])
    plt.axis('off')
    plt.text(0,0, prefix, fontsize=fontsize)
    return ax

  def title(self, title='', fontdict=None, loc='center', pad=None, **kwargs):
    plt.title( title, fontdict=fontdict, loc=loc, pad=pad, **kwargs)
  
  def figtitle(self, title, **kwargs):
    self.fig.suptitle( title, **kwargs )

  def show(self):
    plt.show()

  def get_ylim(self):
    return self.ax.get_ylim()

  def get_xlim(self):
    return self.ax.get_xlim()
  
  def get_xticks(self):
    return self.ax.get_xticks()

  def get_yticks(self):
    return self.ax.get_yticks()
  
  def savefig(self, fname, dpi=None, facecolor='white', edgecolor='white', bbox_inches='tight', **kwargs ):
    import os
    dirname = os.path.dirname(fname)
    mkdirs(dirname)
    plt.savefig(fname,dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, bbox_inches=bbox_inches ,**kwargs)
  
  # def savefig2(self, fname, dpi=None, facecolor='white', edgecolor='white', bbox_inches='tight',
               # base= os.path.join(os.environ['HOME'], 'Projects'), 
               # path2=os.path.join(os.environ['HOME'], 'Nut', 'Projects'),
               # **kwargs ):
    # import os
    # thecwd = os.getcwd()
    # base   = base
    # relcwd = os.path.relpath(thecwd, base)
    # if relcwd == '.':
      # relcwd == ''
    # path2 = path2
    # final_path = os.path.join(path2,relcwd,fname)
    # dirname = os.path.dirname(final_path)
    # mkdirs(dirname)
    # plt.savefig(final_path,dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, bbox_inches=bbox_inches ,**kwargs)

  def xticks_fontsize(self, fontsize):
    for xtick in self.ax.xaxis.get_major_ticks():
      xtick.label.set_fontsize(fontsize) 

  def xticks_padding(self, pad):
    for xtick in self.ax.xaxis.get_major_ticks():
      xtick.set_pad(pad)

  def yticks_padding(self, pad):
    for ytick in self.ax.yaxis.get_major_ticks():
      ytick.set_pad(pad)

  def yticks_fontsize(self, fontsize):
    for xtick in self.ax.yaxis.get_major_ticks():
      xtick.label.set_fontsize(fontsize)
  
  def bmapax(self,lat0=-90,lat1=90,
             lon0=0,lon1=360,
             show_coastline=True,
             show_dashes=False,
             show_colorbar=True,alpha=None,latticks=[-60, 0, 60], lonticks=[0, 60, 120, 180, 240, 300 ],
             lats_fontsize=15, lons_fontsize=15,
             lats_padding=1.6, lons_padding=1.6,**kwargs):
    from mpl_toolkits.basemap import Basemap
    map0 = Basemap(resolution='c',area_thresh=1000,llcrnrlat=float(lat0),llcrnrlon=float(lon0),urcrnrlat=float(lat1),
                   urcrnrlon=float(lon1),ax=self.ax, **kwargs)
    if show_coastline:
      map0.drawcoastlines()
    if show_dashes != True:
      dashes = [1,1000000]
    else:
      dashes = [5,8]
    map0.drawparallels(latticks,labels=[True,False,False,False],dashes=dashes,fontsize=lats_fontsize,xoffset=lats_padding)
    map0.drawmeridians(lonticks,labels=[False,False,False,True],dashes=dashes,fontsize=lons_fontsize,yoffset=lons_padding)
    return map0
   
  def mapshow(self, lats, lons, arr,**kwargs):
    if lats.shape != arr.shape and lons.shape!= arr.shape:
      llons, llats = np.meshgrid(lons, lats)
    else:
      llons, llats = lons, lats
    cbar = self.ax.pcolormesh(llons, llats, arr, **kwargs)
    return cbar
  
  def shade(self, x, y, where=None, ylims=None, color=None):
    if ylims == None:
      ylims = self.get_ylim()
    self.ax.fill_between(x, y, y2=ylims[0], where=where, color=color)
    plt.ylim(*ylims)

def bmapax(ax,lat0=-90,lat1=90,
           lon0=0,lon1=360,
           show_coastline=True,
           show_dashes=False,
           show_colorbar=True,alpha=None,latticks=[-60, 0, 60], lonticks=[0, 60, 120, 180, 240, 300 ],
           lats_fontsize=15, lons_fontsize=15,
           lats_padding=1.6, lons_padding=1.6,**kwargs):
  from mpl_toolkits.basemap import Basemap
  map0 = Basemap(resolution='c',area_thresh=1000,llcrnrlat=float(lat0),llcrnrlon=float(lon0),urcrnrlat=float(lat1),
                 urcrnrlon=float(lon1),ax=ax, **kwargs)
  if show_coastline:
    map0.drawcoastlines()
  if show_dashes != True:
    dashes = [1,1000000]
  else:
    dashes = [5,8]
  map0.drawparallels(latticks,labels=[True,False,False,False],dashes=dashes,fontsize=lats_fontsize,xoffset=lats_padding)
  map0.drawmeridians(lonticks,labels=[False,False,False,True],dashes=dashes,fontsize=lons_fontsize,yoffset=lons_padding)
  return map0
   
def mapshow(ax, lats, lons, arr,**kwargs):
  if lats.shape != arr.shape and lons.shape!= arr.shape:
    llons, llats = np.meshgrid(lons, lats)
  else:
    llons, llats = lons, lats
  llons, llats = np.meshgrid(lons, lats)
  cbar = ax.pcolormesh(llons, llats, arr, **kwargs)
  return cbar

def bmap(lat0=-90,lat1=90,
           lon0=0,lon1=360,
           show_coastline=True,
           show_dashes=False,
           **kwargs):
  from mpl_toolkits.basemap import Basemap
  map0 = Basemap(resolution='c',area_thresh=1000,
                 llcrnrlat=float(self.lat0),llcrnrlon=float(self.lon0),
                 urcrnrlat=float(self.lat1),urcrnrlon=float(self.lon1),
                 **kwargs)
  if show_coastline:
    map0.drawcoastlines()
  if show_dashes != True:
    dashes = [1,1000000]
  else:
    dashes = [5,8]
  self.map = map0
