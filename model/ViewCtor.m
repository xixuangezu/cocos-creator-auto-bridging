
#if $nodeType == "btn"
    -- ${nodeLog} 按钮
#else
    -- ${nodeLog}
#end if
    self.${nodeName} = creatorReader:findChild("${nodeName}")
#if $nodeType == "btn"
    local function _${nodeName}Func(sender)
        self:${nodeName}Func(sender)
    end
    self.${nodeName}:addClickEventListener(_${nodeName}Func)
#end if
