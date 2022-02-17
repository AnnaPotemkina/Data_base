<?php


namespace App;


class BasketAddition
{
    private Database $database;

    private Session $session;

    public function __construct(Database $database, Session $session)
    {
        $this->database = $database;
        $this->session = $session;
    }

    public function BasketAddition(array $product): bool{

        $basket_ids = $this->database->getConnection()->query(
            "SELECT Basket_id, Customer_id FROM Basket"
        )->fetchAll();
        foreach ($basket_ids as $basket_id){
            if ($this->session->getData("user")["user_id"] == $basket_id["Customer_id"]){
                $required_id = $basket_id["Basket_id"];
                break;
            }
        }


        $statement = $this->database->getConnection()->prepare(
            "INSERT INTO Basket_Product (Product_id, Basket_id)
            VALUES (:product_id, :basket_id)"
        );
        $statement->execute([
            "product_id" => $product["product_id"],
            "basket_id" => $required_id
            //"size_id" => $required_id2
        ]);

        return true;
    }
}