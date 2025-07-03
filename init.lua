-- Config for Cmd+E+E to focus Warp
local hyper = {"cmd"}
local doubleTapTimer = nil
local doubleTapThreshold = 0.3 -- seconds
local firstTap = false

hs.hotkey.bind(hyper, "e", function()
    if firstTap then
        -- Second tap detected within threshold
        firstTap = false
        if doubleTapTimer then
            doubleTapTimer:stop()
            doubleTapTimer = nil
        end

        -- Focus or launch Warp
        local app = hs.application.find("Warp")
        if app then
            app:activate()
        else
            hs.application.launchOrFocus("Warp")
        end
    else
        -- First tap
        firstTap = true
        doubleTapTimer = hs.timer.doAfter(doubleTapThreshold, function()
            firstTap = false
        end)
    end
end)