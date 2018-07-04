$stdout.sync = true
require 'sinatra'
require 'httparty'
require 'rubygems'
require 'meli'
require 'json'

class GiftBasket < Sinatra::Base
  attr_reader :tokens

  #meli
  APP_ID = 8357875269029285
  APP_SECRET = "DfjYyjbqO9HDAOQOKmP89NWfsMapPfm2"
  APP_URL = "513e3d91.ngrok.io"
  ACCESS_TOKEN = nil
  REFRESH_TOKEN = nil
  $resultado = 0
  meli = Meli.new(APP_ID, "#{APP_SECRET}")
  disable :reload

  def initialize
    @tokens = {}
    super
  end

  get '/login' do
    install_url = "#{meli.auth_url("https://#{APP_URL}/authorize")}"
    redirect install_url
  end

  get '/authorize' do
    content_type :text
    meli.authorize(params["code"], "https://#{APP_URL}/authorize")
    ACCESS_TOKEN = meli.access_token
    REFRESH_TOKEN = meli.refresh_token
    puts "Autenticación de Meli realizada correctamente! Token: #{meli.access_token} RefresToken: #{meli.refresh_token}"
    get_all_products
    install_url = "https://#{APP_URL}/dataset"
    redirect install_url  
  end           

  get '/dataset' do
    content_type :json
    $tempfinal.to_json
  end 


  helpers do
    def get_all_products
		puts "------------------Buscando el dataset-----------------------"
		meli = Meli.new(APP_ID, "#{APP_SECRET}", "#{ACCESS_TOKEN}", "#{REFRESH_TOKEN}")                   
		user = meli.get("/users/me?access_token=#{ACCESS_TOKEN}")
		res = JSON.parse user.body
		user_id = res["id"]
		columnas = ["id","title", "price", "sold_quantity"]
		query1 = "eagle warrior g16"
		#marca="eagle warrior"
		total = 1
		var = 0
		num = 0 
		#ipad air
		#chromecast
		#iphone 8
		#note8
		#galaxy s8
		productsmeli = meli.get("/sites/MLM/search?q=#{query1}")
		res = JSON.parse productsmeli.body
		total = res["paging"]["total"]
		$tempfinal = []
	    while total > var
	        productsmeli = meli.get("/sites/MLM/search?q=#{query1}&offset=#{var}")
	        $dataset = JSON.parse productsmeli.body
	        #$dataset["results"].delete_if {|producto| producto.dig("attributes",0,"value_name")!="#{marca}"}
	        $dataset["results"].each do |producto|
				producto.each_key  do |columna|
					unless columnas.include?("#{columna}")
						producto.delete("#{columna}")
					end
				end
	        	$tempfinal.push(producto) 
	        	query = meli.get("items/#{producto["id"]}?access_token=#{ACCESS_TOKEN}")
	        	res = JSON.parse query.body
	        	if res.dig("pictures",0)
                	print "#{num} " 
	        		url = res["pictures"][0]["url"]
	                File.open("#{num}.jpg", "wb") do |f| 
	                  f.write HTTParty.get(url).body
	                end
					num = num+1
	        	end
	        end
	        break if num>150
			var = var+50
			puts "Pagina terminada"
	    end



#bundle exec ruby dataset.rb
#./ngrok http 4567



=begin
          dataset["title"] = res["title"]
          dataset["price"] = res["price"]
          dataset["sold_quantity"] = res["sold_quantity"]
		#query = meli.get("/sites/MLM/search?q=chromecast")
		query = meli.get("/users/#{user_id}/items/search?sku=4397400&status=active&access_token=#{ACCESS_TOKEN}")


if res["attributes"][0]["value_name"]=="Samsung"
else
  puts "producto descartado #{res["attributes"][0]["value_name"]}"
end




          dataset["title"] = res["title"]
          dataset["price"] = res["price"]
          dataset["initial_quantity"] = res["initial_quantity"]
          dataset["available_quantity"] = res["available_quantity"]
          dataset["sold_quantity"] = res["sold_quantity"]



		#query = meli.get("/sites/MLM/search?q=chromecast")
		query = meli.get("/users/#{user_id}/items/search?sku=4397400&status=active&access_token=#{ACCESS_TOKEN}")
		res = JSON.parse query.body
		res.to_json
=end

    puts "------------------termino de buscar el dataset-----------------------"
    end
  end
end
run GiftBasket.run!