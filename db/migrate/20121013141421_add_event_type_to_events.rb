class AddEventTypeToEvents < ActiveRecord::Migration
  def change
    add_column :events, :event_type, :text
    add_column :events, :window, :text
  end
end
