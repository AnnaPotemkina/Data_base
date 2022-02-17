<?php


namespace App;


class Buy
{
    private Database $database;

    private Session $session;

    public function __construct(Database $database, Session $session)
    {
        $this->database = $database;
        $this->session = $session;
    }

    public function Buy( array $args): bool{

        $basket_ids = $this->database->getConnection()->query(
            "WITH basket_user as(
        SELECT Basket.Basket_id, Basket_Product.Product_id FROM Basket 
        	JOIN Basket_Product on Basket.Basket_id = Basket_Product.Basket_id
        WHERE Basket.Customer_id = {$args["user_id"]}
        )
    SELECT Code, Type_furniture, Price, Product.Product_id, Available_number FROM Product 
    JOIN basket_user on basket_user.Product_id = Product.Product_id"
        )->fetchAll();
        foreach ($basket_ids as $basket_id) {
            $statement = $this->database->getConnection()->prepare(
                "UPDATE Product SET Available_number = Available_number-1 
                        WHERE Product_id = :basket_id"
            );
            $statement->execute([
                "basket_id" => $basket_id["Product_id"]
                //"size_id" => $required_id2
            ]);
        }

        return true;
    }
}