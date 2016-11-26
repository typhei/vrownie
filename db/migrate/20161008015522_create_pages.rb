class CreatePages < ActiveRecord::Migration[5.0]
  def change
    create_table :pages do |t|
      t.integer :number
      t.string :title
      t.string :url
      t.string :image
      t.string :body
      t.string :site_name
      t.string :date

      t.timestamps
    end
  end
end
