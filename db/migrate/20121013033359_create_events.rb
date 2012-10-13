class CreateEvents < ActiveRecord::Migration
  def change
    create_table :events do |t|
      t.text :word
      t.text :date
      t.text :time

      t.timestamps
    end
  end
end
