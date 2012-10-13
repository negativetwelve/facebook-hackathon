class Event < ActiveRecord::Base
  attr_accessible :date, :time, :word, :window
  
  def word_frequency(events)
    data = []
    events.each do |e|
      date = Time.parse(e.date.to_s + " " + e.time.to_s)-7.hours
      t = (Time.now - date).to_i/60
      if t < 60
        if data[t].nil?
          data[t] = 1
        else
          data[t] += 1
        end
      end
    end
    return data
  end
  
  def click_position(events)
    data = []
    (0..9).each do |i|
      (0..9).each do |j|
        data[i*10+j] = [i*128, j*80, 0]
      end
    end
    events.each do |e|
      pos = e.word.split(",")
      data[pos[0].to_i/128*10 + pos[1].to_i/80][2] += 1
    end
    return data
  end
  
  def time_track(events)
    apps = []
    time = []
    data = [apps, time]
    events.each do |e|
      if data[0].include?(e.window)
        data[1][data[0].index(e.window)] += e.duration
      else
        data[0].append(e.window)
        data[1].append(e.duration)
      end
    end
    return data
  end
  
end
