<?php

use App\Database;
use App\Authorization;
use App\AuthorisationException;
use App\Addition;
use App\Buy;
use App\BasketDelete;
use App\BasketAddition;
use App\Session;
use \Psr\Http\Server\RequestHandlerInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Slim\Factory\AppFactory;
use \Twig\Loader\FilesystemLoader;
use \Twig\Environment;

require __DIR__.'/vendor/autoload.php';

$loader = new FilesystemLoader('templates');
$twig = new Environment($loader);

$app = AppFactory::create();
$app->addErrorMiddleware(true, true, true);
$app->addBodyParsingMiddleware(); // $_POST

$session = new Session();

$sessionMiddleware = function (ServerRequestInterface $request, RequestHandlerInterface $handler) use($session){
    $session->start();
    $response = $handler->handle($request);
    $session->save();
    var_dump($_SESSION);
    return $response;
};

$app->add($sessionMiddleware);

$config = include_once 'config/database.php';
$dsn = $config['dsn'];
$username = $config['username'];
$password = $config['password'];


$database = new Database($dsn, $username, $password);
$authorisation = new Authorization($database, $session);
$addition = new Addition($database, $session);
$BasketAddition = new BasketAddition($database, $session);
$Buy = new Buy($database, $session);
$BasketDelete = new BasketDelete($database, $session);

$app->get('/', function(ServerRequestInterface $request, ResponseInterface $response) use ($twig, $session) {

    $body = $twig->render('index.twig',[
        'user' => $session->getData('user')
    ]);
    $response->getBody()->write($body);

    return $response;
});

$app->get('/login/', function(ServerRequestInterface $request, ResponseInterface $response) use ($twig, $session) {

    $body = $twig->render('login.twig', [
        "message" => $session->flush('message'),
        "form" => $session->flush('form')
    ]);
    $response->getBody()->write($body);

   return $response;
});

$app->post('/login-post/', function(ServerRequestInterface $request, ResponseInterface $response) use($authorisation, $session) {
    $params = (array) $request->getParsedBody();

    try {
            $authorisation->login($params['email'], $params['password']);
    } catch (AuthorisationException $exception){
        $session->setData('message', $exception->getMessage());
        $session->setData('form', $params);

        return $response->withHeader('Location', '/login/')
            ->withStatus(302);
    }
    return $response->withHeader('Location', '/')
        ->withStatus(302);
});

$app->get('/register/', function(ServerRequestInterface $request, ResponseInterface $response) use ($twig, $database, $session) {
    $types = $database->getConnection()->query(
        "SELECT type_name FROM Types"
    )->fetchAll();
    $body = $twig->render('register.twig', [
        "types" => $types,
        "message" => $session->flush('message'),
        "form" => $session->flush('form')
    ]);

    $response->getBody()->write($body);

    return $response;
});

$app->post('/register-post/', function(ServerRequestInterface $request, ResponseInterface $response) use($authorisation, $session) {
    $params = (array) $request->getParsedBody();
    try {
        $authorisation->register($params);
    } catch (AuthorisationException $exception){
        $session->setData('message', $exception->getMessage());
        $session->setData('form', $params);
        return $response->withHeader('Location', '/register/')
            ->withStatus(302);
    }

    return $response->withHeader('Location', '/')
        ->withStatus(302);
});

$app->get('/logout/', function(ServerRequestInterface $request, ResponseInterface $response) use ($session) {
    $admin = 1;
    $session->setData('user', null);
    return $response->withHeader('Location','/')
        ->withStatus(302);
});

$app->get('/admin/', function(ServerRequestInterface $request, ResponseInterface $response) use ($twig, $session) {

    $body = $twig->render('admin.twig', ["user" => $session->getData("user")]);
    $response->getBody()->write($body);

    return $response;
});

$app->get('/addproduct/', function(ServerRequestInterface $request, ResponseInterface $response) use ($twig, $session, $database) {
    $types = $database->getConnection()->query(
        "SELECT type_name FROM Types"
    )->fetchAll();
    $Sizes = $database->getConnection()->query(
        "SELECT * FROM Sizes"
    )->fetchAll();
    $body = $twig->render('addproduct.twig',[
        "types" => $types, "Sizes" => $Sizes, "user" => $session->getData("user")]);
    $response->getBody()->write($body);

    return $response;
});

$app->post('/addproduct-post/', function(ServerRequestInterface $request, ResponseInterface $response) use($addition, $session) {
    $params = (array) $request->getParsedBody();

    try {
        $addition->addition($params);
    } catch (AuthorisationException $exception){
        $session->setData('message', $exception->getMessage());
        $session->setData('form', $params);
        return $response->withHeader('Location', '/addproduct/')
            ->withStatus(302);
    }

    return $response->withHeader('Location', '/')
        ->withStatus(302);
});

$app->get('/showuser/', function(ServerRequestInterface $request, ResponseInterface $response) use ($twig, $database, $session) {
    $customer = $database->getConnection()->query(
        "SELECT Organisation_name, Phone_number, Customer_email FROM Customer"
    )->fetchAll();
    $body = $twig->render('showuser.twig', [
        "customer" => $customer,
        "message" => $session->flush('message'),
        "form" => $session->flush('form'),
        "user" => $session->getData("user")
    ]);

    $response->getBody()->write($body);

    return $response;
});

$app->get('/catalog/', function(ServerRequestInterface $request, ResponseInterface $response) use ($twig, $database, $session) {
    $product = $database->getConnection()->query(
        "SELECT Code, Type_furniture, Price, Product_id FROM Product"
    )->fetchAll();
    $body = $twig->render('catalog.twig', [
        "product" => $product,
        "message" => $session->flush('message'),
        "form" => $session->flush('form'),
        "user" => $session->getData("user")
    ]);

    $response->getBody()->write($body);

    return $response;
});

$app->get('/read-more-product/{product_id}/', function(ServerRequestInterface $request, ResponseInterface $response, $args) use ($twig, $database, $session) {
    $product = $database->getConnection()->query(
        "SELECT Code, Type_furniture, Price, Available_number, Product_id FROM Product
                    WHERE Product_id = {$args["product_id"]}"
    )->fetchAll();
    $body = $twig->render('read-more-product.twig', [
        "product" => $product,
        "message" => $session->flush('message'),
        "form" => $session->flush('form'),
        "user" => $session->getData("user")
    ]);

    $response->getBody()->write($body);

    return $response;
});

$app->get('/basket-person-post/{product_id}/', function(ServerRequestInterface $request, ResponseInterface $response, $args) use ($BasketAddition, $twig, $database, $session) {
    try {
        $BasketAddition->BasketAddition($args);
    } catch (AuthorisationException $exception){
        $session->setData('message', $exception->getMessage());
        return $response->withHeader('Location', "/read-more-product/{$args["product_id"]}/")
            ->withStatus(302);
    }

    return $response->withHeader('Location', "/read-more-product/{$args["product_id"]}/")
        ->withStatus(302);
});

$app->get('/basket/{user_id}/', function(ServerRequestInterface $request, ResponseInterface $response, $args) use ($twig, $database, $session) {
    $product = $database->getConnection()->query(
        "WITH basket_user as(
        SELECT Basket.Basket_id, Basket_Product.Product_id, Basket_Product.Basket_Product_id FROM Basket 
        	JOIN Basket_Product on Basket.Basket_id = Basket_Product.Basket_id
        WHERE Basket.Customer_id = {$args["user_id"]}
        )
    SELECT Code, Type_furniture, Price, Product.Product_id, Available_number, Basket_Product_id FROM Product 
    JOIN basket_user on basket_user.Product_id = Product.Product_id"
    )->fetchAll();
    $body = $twig->render('basket.twig', [
        "product" => $product,
        "message" => $session->flush('message'),
        "form" => $session->flush('form'),
        "user" => $session->getData("user")
    ]);

    $response->getBody()->write($body);

    return $response;
});

$app->get('/basket-post/{user_id}/', function(ServerRequestInterface $request, ResponseInterface $response, $args) use ($Buy, $BasketAddition, $twig, $database, $session) {
    try {
        $Buy->Buy($args);
    } catch (AuthorisationException $exception){
        $session->setData('message', $exception->getMessage());
        return $response->withHeader('Location', "/basket/{$args["user_id"]}/")
            ->withStatus(302);
    }

    return $response->withHeader('Location', "/basket/{$args["user_id"]}/")
        ->withStatus(302);
});

$app->get('/basket-post-delete/{ basket_product_id }/', function(ServerRequestInterface $request, ResponseInterface $response, $args) use ($BasketDelete, $twig, $database, $session) {
    try {
        $BasketDelete->BasketDelete($args);
    } catch (AuthorisationException $exception){
        $session->setData('message', $exception->getMessage());
        return $response->withHeader('Location', "/basket/{$session->getData("user")["user_id"]}/")
            ->withStatus(302);
    }

    return $response->withHeader('Location', "/basket/{$session->getData("user")["user_id"]}/")
        ->withStatus(302);
});
$app->run();

