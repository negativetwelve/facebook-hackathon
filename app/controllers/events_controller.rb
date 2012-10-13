class EventsController < ApplicationController
  
  def show
    @e = Event.new
    if params[:event_id] == "1"
      @data = @e.word_frequency(Event.all)
    elsif params[:event_id] == "2"
      @data = @e.click_position(Event.where(event_type: "Mouse"))
    elsif params[:event_id] == "3"
      
    end
  end
  
end
