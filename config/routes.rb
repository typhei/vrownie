Rails.application.routes.draw do
  root "home#top"
  get '/top' => 'home#top'
  get '/home/top/:start' => "home#top"
  get '/about' => "home#about"
#  get '/inqury' => "home#inqury"
#  get '/video' => "home#video"
  

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
