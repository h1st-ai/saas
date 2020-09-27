module Controller exposing (..)

import Http
import Json.Decode exposing (Decoder, field, list, string, succeed)
import Json.Decode.Pipeline exposing (optional, required)
import Task exposing (Task)
import Url.Builder as UB


type alias Workbench =
    { id : String
    , user_id : String
    , status : String
    , public_endpoint : String
    , name : String
    }


host : String
host =
    "http://10.30.0.142:8999"



-- host = "http://10.30.128.207:8999"
-- staging


endpoint : String
endpoint =
    UB.custom (UB.CrossOrigin host) [ "workbenches" ] [ UB.string "user_id" "" ] Nothing


workbenchEndpoint : Workbench -> String
workbenchEndpoint wb =
    UB.crossOrigin host [ "workbenches", wb.id ] [ UB.string "user_id" wb.user_id ]


startWorkbenchEndpoint : Workbench -> String
startWorkbenchEndpoint wb =
    UB.crossOrigin host [ "workbenches", wb.id, "start" ] [ UB.string "user_id" wb.user_id ]


stopWorkbenchEndpoint : Workbench -> String
stopWorkbenchEndpoint wb =
    UB.crossOrigin host [ "workbenches", wb.id, "stop" ] [ UB.string "user_id" wb.user_id ]


listWorkbenches : (Result Http.Error (List Workbench) -> a) -> Cmd a
listWorkbenches msg =
    Http.get
        { url = endpoint
        , expect = Http.expectJson msg workbenchListDecoder
        }



-- listWorkbenchesTask : Task Http.Error (List Workbench)
-- listWorkbenchesTask =
--     Http.task {
--         method = "GET"
--         , url = endpoint
--         , headers = []
--         , timeout = Nothing
--         , body = Http.emptyBody
--         , resolver = Http.stringResolver (resolve Ok)
--     }


refreshWorkbench : (Result Http.Error Workbench -> a) -> Cmd a
refreshWorkbench msg =
    Http.get
        { url = endpoint
        , expect = Http.expectJson msg workbenchItemEncoder
        }


startWorkbench : Workbench -> (Result Http.Error Workbench -> a) -> Cmd a
startWorkbench wb msg =
    let
        mapper : Result Http.Error () -> a
        mapper result =
            case result of
                Ok _ ->
                    msg (Ok wb)

                Err err ->
                    msg (Err err)
    in
    Http.post
        { url = startWorkbenchEndpoint wb
        , body = Http.emptyBody
        , expect = Http.expectWhatever mapper
        }


deleteWorkbench : Workbench -> (Result Http.Error Workbench -> a) -> Cmd a
deleteWorkbench wb msg =
    let
        mapper : Result Http.Error () -> a
        mapper result =
            case result of
                Ok _ ->
                    msg (Ok wb)

                Err err ->
                    msg (Err err)
    in
    Http.request
        { method = "DELETE"
        , headers = []
        , url = workbenchEndpoint wb
        , body = Http.emptyBody
        , expect = Http.expectWhatever mapper
        , timeout = Nothing
        , tracker = Nothing
        }


stopWorkbench : Workbench -> (Result Http.Error Workbench -> a) -> Cmd a
stopWorkbench wb msg =
    let
        mapper : Result Http.Error () -> a
        mapper result =
            case result of
                Ok _ ->
                    msg (Ok wb)

                Err err ->
                    msg (Err err)
    in
    Http.post
        { url = stopWorkbenchEndpoint wb
        , body = Http.emptyBody
        , expect = Http.expectWhatever mapper
        }


workbenchListDecoder : Decoder (List Workbench)
workbenchListDecoder =
    field "items" (list workbenchDecoder)


workbenchItemEncoder : Decoder Workbench
workbenchItemEncoder =
    field "item" workbenchDecoder


workbenchDecoder : Decoder Workbench
workbenchDecoder =
    succeed Workbench
        |> required "workbench_id" string
        |> required "user_id" string
        |> required "status" string
        |> optional "public_endpoint" string ""
        |> optional "workbench_name" string ""
