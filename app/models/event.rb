class Event < ActiveRecord::Base
  attr_accessible :date, :time, :word
  
  def word_frequency(events)
    d = DateTime.parse(DateTime.now.to_s)
    @data = []
    events.each do |e|
      date = Time.parse(e.date.to_s + " " + e.time.to_s)-7.hours
      t = (Time.now - date).to_i/60
      if t < 60
        if @data[t].nil?
          @data[t] = 1
        else
          @data[t] += 1
        end
      end
    end
    return @data
  end
  
  def click_position(events)
  
  
end
