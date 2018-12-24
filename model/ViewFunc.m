
#if $nodeType == "node"
-- getter: ${nodeLog}
function UiView${rootName}:get${nodeName}()
    return self.${nodeName}
end
#else if $nodeType == "btn" and $funcType == "getFunc"
-- getter: ${nodeLog} 按钮
function UiView${rootName}:get${nodeName}()
    return self.${nodeName}
end
#else if $nodeType == "btn" and $funcType == "callFunc"
-- 按钮 ${nodeLog}
function UiView${rootName}:${nodeName}Func(sender)
    print("点击按钮 ${nodeLog}")
end
#end if
