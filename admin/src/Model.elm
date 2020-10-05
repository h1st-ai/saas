module Model exposing (Model, mergeWorkbenches, updateWorkbench)

import Controller exposing (Workbench)
import Dict


type alias Model =
    { image : Maybe String
    , error : String
    , workbenches : Dict.Dict String Workbench
    , selectedWorkbench : Maybe Workbench
    }


mergeWorkbenches : Model -> List Workbench -> Model
mergeWorkbenches model listWorkbenches =
    let
        wbDict =
            Dict.fromList (List.map (\w -> ( w.id, w )) listWorkbenches)
    in
    { model | workbenches = Dict.union wbDict model.workbenches }


updateWorkbench : Model -> Workbench -> Model
updateWorkbench model wb =
    { model | workbenches = Dict.insert wb.id wb model.workbenches }
