class EventsController < ApplicationController
  
  def show
    @events = Event.all
    @e = Event.new
    if params[:event_id] == "1"
      @data = @e.word_frequency(@events)
    elsif params[:event_id] == "2"
      @data = @e.click_position(@events)
    elsif params[:event_id] == "3"
      
    end
  end
  
end
