module Main exposing (main)

import Browser
import Controller as C exposing (Workbench)
import Debug
import Dict exposing (Dict)
import Html exposing (Html, a, button, div, img, span, table, tbody, td, text, th, thead, tr)
import Html.Attributes exposing (class, href, src, style, target)
import Html.Events exposing (onClick)
import Http
import Model exposing (Model, mergeWorkbenches)


main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = subscriptions
        }


init : () -> ( Model, Cmd Msg )
init _ =
    ( { image = Nothing
      , workbenches = Dict.empty
      , error = ""
      }
    , C.listWorkbenches GotWorkbenches
    )



-- UPDATE


type Msg
    = Loading
    | GotWorkbenches (Result Http.Error (List C.Workbench))
    | GotWorkbenchUpdate (Result Http.Error C.Workbench)
    | GotWorkbenchDeleted (Result Http.Error C.Workbench)
    | ClickedRefreshWorkbench
    | ClickedStartWorbench C.Workbench
    | ClickedStopWorkbench C.Workbench
    | ClickedDeleteWorkbench C.Workbench


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Loading ->
            ( model, Cmd.none )

        GotWorkbenches wb ->
            case wb of
                Ok wbList ->
                    ( mergeWorkbenches model wbList, Cmd.none )

                Err err ->
                    ( { model | error = Debug.toString err }, Cmd.none )

        ClickedStartWorbench wb ->
            let
                wbs =
                    Dict.insert wb.id { wb | status = "starting" } model.workbenches
            in
            ( { model | workbenches = wbs }, C.startWorkbench wb GotWorkbenchUpdate )

        ClickedStopWorkbench wb ->
            let
                wbs =
                    Dict.insert wb.id { wb | status = "stopping" } model.workbenches
            in
            ( { model | workbenches = wbs }, C.stopWorkbench wb GotWorkbenchUpdate )

        ClickedRefreshWorkbench ->
            ( model, C.listWorkbenches GotWorkbenches )

        ClickedDeleteWorkbench wb ->
            ( model, C.deleteWorkbench wb GotWorkbenchDeleted )

        GotWorkbenchUpdate wb ->
            case wb of
                Ok _ ->
                    ( model, Cmd.none )

                Err err ->
                    ( { model | error = Debug.toString err }, Cmd.none )

        GotWorkbenchDeleted res ->
            case res of
                Ok wb ->
                    ( { model | workbenches = Dict.remove wb.id model.workbenches }, Cmd.none )

                Err _ ->
                    ( model, Cmd.none )



-- SUBSCRIPTION


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    div [ class "container-xl" ]
        [ div [ style "padding" "5px" ]
            [ button [ class "btn btn-secondary", onClick ClickedRefreshWorkbench ] [ text "Refresh" ]
            ]
        , viewError model
        , viewTable model
        ]


viewError : Model -> Html Msg
viewError model =
    if model.error /= "" then
        div [ class "alert alert-warning" ] [ text model.error ]

    else
        div [] []


viewTable : Model -> Html Msg
viewTable model =
    table [ class "table table-sm table-striped" ]
        [ thead [ class "thead-dark" ]
            [ tr []
                [ th [] [ text "ID" ]
                , th [] [ text "Name" ]
                , th [] [ text "Status" ]
                , th [] [ text "" ]
                ]
            ]
        , tbody [] (List.map viewRow (Dict.toList model.workbenches))
        ]


viewRow : ( String, C.Workbench ) -> Html Msg
viewRow ( _, wb ) =
    tr []
        [ td [] [ a [ href wb.public_endpoint, target "_blank" ] [ text wb.id ] ]
        , td []
            [ text wb.name
            , div [ class "subtitle" ] [ text wb.user_id ]
            ]
        , td []
            [ if wb.status == "running" then
                span [ class "badge badge-primary" ] [ text wb.status ]

              else
                span [ class "badge badge-secondary" ] [ text wb.status ]
            ]
        , td [] (viewRowActions wb)
        ]


viewRowActions : C.Workbench -> List (Html Msg)
viewRowActions wb =
    [ if wb.status == "stopped" then
        button [ class "btn btn-sm btn-outline-secondary", onClick (ClickedStartWorbench wb) ] [ text "start" ]

      else
        button [ class "btn btn-sm btn-outline-secondary", onClick (ClickedStopWorkbench wb) ] [ text "stop" ]
    , text " "
    , button [ class "btn btn-sm btn-outline-danger", onClick (ClickedDeleteWorkbench wb) ] [ text "delete" ]
    ]
