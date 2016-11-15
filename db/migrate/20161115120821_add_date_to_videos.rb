class AddDateToVideos < ActiveRecord::Migration[5.0]
  def change
    add_column :videos, :Date, :integer
  end
end
