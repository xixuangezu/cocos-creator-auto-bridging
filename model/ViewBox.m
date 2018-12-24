-- Ui view ${startLog}
local UiView${rootName} = class("UiView${rootName}")

##ctor()
function UiView${rootName}:ctor(_scene)

#if $rootType == "rootP"
    local creatorReader = _scene.creatorReader_
    self._scene = _scene
    self.vRoot = creatorReader:findChild("${rootName}")
#else if $rootType == "rootN"
    local creatorReader = creator.CreatorReader:createWithFilename('creator/Scenes/${fileName}.ccreator')
    self._scene = _scene
    creatorReader:setup()
    creatorReader:getSceneGraph()

    local vRoot = creatorReader:findChild("${rootName}")
    vRoot:retain()
    vRoot:removeFromParent()
    vRoot:autorelease()
    self.vRoot = vRoot
#end if
    self.vRoot.luaClass = self
##
${ctorBody}
##
    if self.onCreate then self:onCreate() end
end
##ctor()end

-- getter: <root>
function UiView${rootName}:getRoot()
    return self.vRoot
end
##
${funcBody}
##
return UiView${rootName}