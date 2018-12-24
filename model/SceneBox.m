-- 场景 ${startLog}
local ${rootName} = class("${rootName}", require("app.ui.SceneBase"))

function ${rootName}:onCreate(data)

	self.page${rootName} = require("app.views.UiLogic${rootName}"):create(self)
end

return ${rootName}