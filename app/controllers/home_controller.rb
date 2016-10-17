# coding: utf-8
class HomeController < ApplicationController
  def top
    @ad = 1
    i = Page.maximum(:number)
    count = 1
    @page = []
    #@toparticle1 = Page.find_by(:number => i)
    #@toparticle2 = Page.find_by(:number => i-1)
    @start = params[:start].to_i
    if @start < 1 then
      @start = 1
    end
    if !@start.nil? then
      i -= (@start-1)*40
    end
    while(!(Page.find_by(:number => i).nil?)) do
      @page.push(Page.find_by(:number => i))
      i-=1
      count += 1
      if count > 40 then
        break
      end
    end


    #検索フォームに入力があれば、その条件でタスクを取得
    if params[:title].present?
      @page = Page.all
      @page = @page.where(@page.arel_table[:title].matches("%#{params[:title]}%"))
    end

  end

  def about
    @ad = 1
  end

  def inqury
  end
  
  def video
  end

end
