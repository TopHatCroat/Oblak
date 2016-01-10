class CreateFileItems < ActiveRecord::Migration
  def change
    create_table :file_items do |t|
      t.string :name
      t.string :attachment
      t.float :size

      t.timestamps null: false
    end
  end
end
