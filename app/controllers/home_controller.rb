# coding: utf-8
class HomeController < ApplicationController
  def top
    @ad = 1
    @page = Page.order("number").reverse_order.page(params[:page]).per(40)

  end

  def about
    @ad = 1
  end

  def inquiry
  end
  
  def video
    @ad = 1
    @video = Video.order("id").reverse_order.page(params[:page]).per(40)
  end

end
