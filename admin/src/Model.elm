module Model exposing (Model, mergeWorkbenches, updateWorkbench, removeWorkbench)

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
            Dict.fromList (List.map (\w -> ( w.user_id ++ " " ++ w.id, w )) listWorkbenches)
    in
    { model | workbenches = Dict.union wbDict model.workbenches }


updateWorkbench : Model -> Workbench -> Model
updateWorkbench model w =
    { model | workbenches = Dict.insert (w.user_id ++ " " ++ w.id) w model.workbenches }

removeWorkbench : Model -> Workbench -> Model
removeWorkbench model w =
    { model | workbenches = Dict.remove (w.user_id ++ " " ++ w.id) model.workbenches } 