class CreateVideos < ActiveRecord::Migration[5.0]
  def change
    create_table :videos do |t|
      t.string :title
      t.string :url
      t.string :image
      t.string :site_name

      t.timestamps
    end
  end
end
