class EventsController < ApplicationController
  
  def show
    @e = Event.new
    if params[:event_id] == "1"
      @data = @e.word_frequency(Event.where(event_type: "WORD"))
    elsif params[:event_id] == "2"
      @data = @e.click_position(Event.where(event_type: "Mouse"))
    elsif params[:event_id] == "3"
      @data, @data2 = @e.time_track(Event.where(event_type: "Screen"))
    end
  end
  
end
