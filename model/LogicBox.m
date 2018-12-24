-- Ui逻辑 ${startLog}
local UiLogic${rootName} = class( "UiLogic${rootName}", require("app.views.UiView${rootName}"))
local UiUtil = require("app.util.UiUtil")

function UiLogic${rootName}:onCreate(data)
##
${onCreateBody}
##
end
##
${funcBody}
##
return UiLogic${rootName}